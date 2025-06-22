from celery import Celery
import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
from datetime import datetime
import sqlite3
import redis
import re
from typing import Dict, List, Any, Optional
import hashlib
from collections import Counter

# Celery app configuration
app = Celery(
    "worker",
    broker=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://localhost:6379/0")
)

# Redis connection
redis_client = redis.from_url(os.environ.get('REDIS_URL', 'redis://redis:6379/0'))

def get_db_connection():
    """Get database connection"""
    # Share database file with API via volume
    db_path = "/app/app.db"
    return sqlite3.connect(db_path)

def update_task_status(task_id, status, result=None, error=None):
    """Update task status in database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if status == "completed":
            cursor.execute(
                "UPDATE tasks SET status = ?, result = ?, completed_at = ? WHERE id = ?",
                (status, result, datetime.utcnow().isoformat(), task_id)
            )
        elif status == "failed":
            cursor.execute(
                "UPDATE tasks SET status = ?, error = ?, completed_at = ? WHERE id = ?",
                (status, error, datetime.utcnow().isoformat(), task_id)
            )
        else:
            cursor.execute(
                "UPDATE tasks SET status = ? WHERE id = ?",
                (status, task_id)
            )
        
        conn.commit()
        conn.close()
        print(f"Updated task {task_id} status to {status}")
    except Exception as e:
        print(f"Error updating task status: {e}")

def extract_content(url):
    """Extract content from a single URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        print(f"Fetching URL: {url}")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract basic info
        title = soup.find('title')
        title_text = title.get_text().strip() if title else "No title"
        
        # Extract meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        description = meta_desc.get('content', '') if meta_desc else ''
        
        # Extract headings
        headings = []
        for i in range(1, 4):  # h1 to h3 only
            for heading in soup.find_all(f'h{i}'):
                headings.append({
                    'level': i,
                    'text': heading.get_text().strip()
                })
                if len(headings) >= 10:  # Limit headings
                    break
        
        # Extract some paragraphs
        paragraphs = []
        for p in soup.find_all('p'):
            text = p.get_text().strip()
            if text and len(text) > 20:  # Only meaningful paragraphs
                paragraphs.append(text)
                if len(paragraphs) >= 5:  # Limit paragraphs
                    break
        
        # Extract links
        links = []
        for link in soup.find_all('a', href=True):
            href = link.get('href', '')
            text = link.get_text().strip()
            if href and text:
                full_url = urljoin(url, href)
                parsed = urlparse(full_url)
                if parsed.scheme in ['http', 'https']:
                    links.append({
                        'url': full_url,
                        'text': text[:100],  # Limit text length
                        'internal': parsed.netloc == urlparse(url).netloc
                    })
                    if len(links) >= 20:  # Limit links
                        break
        
        return {
            'url': url,
            'status_code': response.status_code,
            'title': title_text,
            'description': description,
            'headings': headings,
            'paragraphs': paragraphs,
            'links': links,
            'content_length': len(response.content),
            'scraped_at': datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        print(f"Error extracting content from {url}: {e}")
        return {
            'url': url,
            'error': str(e),
            'scraped_at': datetime.utcnow().isoformat()
        }

@app.task(bind=True)
def crawl_url(self, task_id, url, depth=1, max_pages=10):
    """Main crawling task"""
    try:
        print(f"Starting crawl task {task_id} for URL: {url}")
        update_task_status(task_id, "running")
        
        crawled_urls = set()
        to_crawl = [url]
        results = []
        current_depth = 0
        
        while to_crawl and len(results) < max_pages and current_depth < depth:
            current_batch = to_crawl.copy()
            to_crawl = []
            
            for current_url in current_batch:
                if current_url in crawled_urls or len(results) >= max_pages:
                    continue
                
                print(f"Crawling: {current_url}")
                content = extract_content(current_url)
                results.append(content)
                crawled_urls.add(current_url)
                
                # Collect internal links for next level
                if current_depth < depth - 1 and 'links' in content and not content.get('error'):
                    for link in content['links']:
                        if (link.get('internal') and 
                            link['url'] not in crawled_urls and 
                            link['url'] not in to_crawl):
                            to_crawl.append(link['url'])
                
                # Be respectful - small delay
                time.sleep(1)
            
            current_depth += 1
        
        # Prepare final result
        final_result = {
            'task_id': task_id,
            'total_pages': len(results),
            'crawled_urls': list(crawled_urls),
            'pages': results,
            'depth_reached': current_depth,
            'completed_at': datetime.utcnow().isoformat()
        }
        
        # Update task as completed
        result_json = json.dumps(final_result)
        update_task_status(task_id, "completed", result_json)
        
        print(f"Crawl task {task_id} completed successfully. Crawled {len(results)} pages.")
        return final_result
        
    except Exception as e:
        error_msg = f"Crawl task failed: {str(e)}"
        print(f"Error in task {task_id}: {error_msg}")
        update_task_status(task_id, "failed", error=error_msg)
        raise

@app.task
def health_check():
    """Simple health check task"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "worker": "operational"
    }

# Celery configuration
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

class EnhancedWebCrawler:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def analyze_seo(self, soup: BeautifulSoup, url: str) -> Dict[str, Any]:
        """Phân tích SEO của trang web"""
        seo_analysis = {
            "title_length": 0,
            "meta_description": "",
            "meta_description_length": 0,
            "h1_count": 0,
            "h2_count": 0,
            "meta_keywords": "",
            "og_tags": {},
            "schema_markup": [],
            "canonical_url": "",
            "robots_meta": "",
            "lang": "",
            "charset": ""
        }
        
        # Title analysis
        title_tag = soup.find('title')
        if title_tag:
            seo_analysis["title_length"] = len(title_tag.get_text().strip())
            
        # Meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            desc = meta_desc.get('content', '')
            seo_analysis["meta_description"] = desc
            seo_analysis["meta_description_length"] = len(desc)
            
        # Heading counts
        seo_analysis["h1_count"] = len(soup.find_all('h1'))
        seo_analysis["h2_count"] = len(soup.find_all('h2'))
        
        # Meta keywords
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        if meta_keywords:
            seo_analysis["meta_keywords"] = meta_keywords.get('content', '')
            
        # Open Graph tags
        og_tags = soup.find_all('meta', attrs={'property': lambda x: x and x.startswith('og:')})
        for tag in og_tags:
            prop = tag.get('property', '')
            content = tag.get('content', '')
            seo_analysis["og_tags"][prop] = content
            
        # Schema markup
        scripts = soup.find_all('script', attrs={'type': 'application/ld+json'})
        for script in scripts:
            try:
                schema_data = json.loads(script.string)
                seo_analysis["schema_markup"].append(schema_data)
            except:
                pass
                
        # Canonical URL
        canonical = soup.find('link', attrs={'rel': 'canonical'})
        if canonical:
            seo_analysis["canonical_url"] = canonical.get('href', '')
            
        # Robots meta
        robots = soup.find('meta', attrs={'name': 'robots'})
        if robots:
            seo_analysis["robots_meta"] = robots.get('content', '')
            
        # Language
        html_tag = soup.find('html')
        if html_tag:
            seo_analysis["lang"] = html_tag.get('lang', '')
            
        return seo_analysis
    
    def detect_social_media(self, soup: BeautifulSoup) -> Dict[str, List[str]]:
        """Phát hiện liên kết mạng xã hội"""
        social_patterns = {
            'facebook': [r'facebook\.com', r'fb\.com'],
            'twitter': [r'twitter\.com', r'x\.com'],
            'instagram': [r'instagram\.com'],
            'linkedin': [r'linkedin\.com'],
            'youtube': [r'youtube\.com', r'youtu\.be'],
            'tiktok': [r'tiktok\.com'],
            'telegram': [r'telegram\.org', r't\.me'],
            'whatsapp': [r'whatsapp\.com', r'wa\.me'],
            'zalo': [r'zalo\.me'],
            'pinterest': [r'pinterest\.com']
        }
        
        social_links = {platform: [] for platform in social_patterns.keys()}
        
        # Find all links
        links = soup.find_all('a', href=True)
        for link in links:
            href = link.get('href', '').lower()
            for platform, patterns in social_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, href):
                        social_links[platform].append(href)
                        break
                        
        return {k: list(set(v)) for k, v in social_links.items() if v}
    
    def extract_contact_info(self, soup: BeautifulSoup) -> Dict[str, List[str]]:
        """Trích xuất thông tin liên hệ"""
        contact_info = {
            'emails': [],
            'phones': [],
            'addresses': []
        }
        
        text_content = soup.get_text()
        
        # Email pattern
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text_content)
        contact_info['emails'] = list(set(emails))
        
        # Phone patterns (Vietnamese format)
        phone_patterns = [
            r'(\+84|0)[0-9]{9,10}',
            r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',
            r'\b\d{4}[-.\s]?\d{3}[-.\s]?\d{3}\b'
        ]
        
        phones = []
        for pattern in phone_patterns:
            phones.extend(re.findall(pattern, text_content))
        contact_info['phones'] = list(set(phones))
        
        # Address keywords (Vietnamese)
        address_keywords = ['địa chỉ', 'address', 'số', 'đường', 'phường', 'quận', 'thành phố', 'tỉnh']
        
        return contact_info
    
    def analyze_content_quality(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Phân tích chất lượng nội dung"""
        quality_metrics = {
            'word_count': 0,
            'paragraph_count': 0,
            'image_count': 0,
            'video_count': 0,
            'link_count': 0,
            'readability_score': 0,
            'content_freshness': '',
            'language_detected': 'unknown'
        }
        
        # Text analysis
        text_content = soup.get_text()
        words = re.findall(r'\b\w+\b', text_content)
        quality_metrics['word_count'] = len(words)
        
        # Structural elements
        quality_metrics['paragraph_count'] = len(soup.find_all('p'))
        quality_metrics['image_count'] = len(soup.find_all('img'))
        quality_metrics['video_count'] = len(soup.find_all(['video', 'iframe']))
        quality_metrics['link_count'] = len(soup.find_all('a', href=True))
        
        # Simple readability (average words per sentence)
        sentences = re.split(r'[.!?]+', text_content)
        if sentences and words:
            quality_metrics['readability_score'] = len(words) / len([s for s in sentences if s.strip()])
        
        # Language detection (simple heuristic)
        vietnamese_chars = len(re.findall(r'[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]', text_content.lower()))
        if vietnamese_chars > 10:
            quality_metrics['language_detected'] = 'vietnamese'
        elif re.search(r'[a-zA-Z]', text_content):
            quality_metrics['language_detected'] = 'english'
            
        return quality_metrics
    
    def extract_structured_data(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Trích xuất dữ liệu có cấu trúc"""
        structured_data = {
            'breadcrumbs': [],
            'navigation_menu': [],
            'footer_links': [],
            'forms': [],
            'tables': []
        }
        
        # Breadcrumbs
        breadcrumb_selectors = [
            '.breadcrumb a', '.breadcrumbs a', '[aria-label="breadcrumb"] a',
            '.navigation-path a', '.nav-breadcrumb a'
        ]
        
        for selector in breadcrumb_selectors:
            breadcrumbs = soup.select(selector)
            if breadcrumbs:
                structured_data['breadcrumbs'] = [link.get_text().strip() for link in breadcrumbs]
                break
        
        # Navigation menu
        nav_selectors = ['nav a', '.navigation a', '.menu a', '.nav a']
        for selector in nav_selectors:
            nav_links = soup.select(selector)
            if nav_links:
                structured_data['navigation_menu'] = [
                    {'text': link.get_text().strip(), 'href': link.get('href', '')} 
                    for link in nav_links[:20]  # Limit to 20 items
                ]
                break
        
        # Footer links
        footer = soup.find('footer')
        if footer:
            footer_links = footer.find_all('a', href=True)
            structured_data['footer_links'] = [
                {'text': link.get_text().strip(), 'href': link.get('href', '')} 
                for link in footer_links[:15]
            ]
        
        # Forms
        forms = soup.find_all('form')
        for form in forms:
            form_data = {
                'action': form.get('action', ''),
                'method': form.get('method', 'get'),
                'inputs': []
            }
            
            inputs = form.find_all(['input', 'textarea', 'select'])
            for inp in inputs:
                input_data = {
                    'type': inp.get('type', inp.name),
                    'name': inp.get('name', ''),
                    'placeholder': inp.get('placeholder', ''),
                    'required': inp.has_attr('required')
                }
                form_data['inputs'].append(input_data)
            
            structured_data['forms'].append(form_data)
        
        # Tables
        tables = soup.find_all('table')
        for table in tables[:5]:  # Limit to 5 tables
            table_data = {
                'headers': [],
                'rows': 0
            }
            
            headers = table.find_all('th')
            if headers:
                table_data['headers'] = [th.get_text().strip() for th in headers]
            
            table_data['rows'] = len(table.find_all('tr'))
            structured_data['tables'].append(table_data)
        
        return structured_data
    
    def crawl_page_enhanced(self, url: str) -> Dict[str, Any]:
        """Crawl trang với tính năng nâng cao"""
        try:
            print(f"🚀 Enhanced crawling: {url}")
            
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Basic extraction
            title = soup.find('title')
            title_text = title.get_text().strip() if title else ""
            
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            description = meta_desc.get('content', '') if meta_desc else ""
            
            # Enhanced extractions
            page_data = {
                'url': url,
                'title': title_text,
                'description': description,
                'content_size': len(response.content),
                'status_code': response.status_code,
                'crawled_at': datetime.now().isoformat(),
                
                # Enhanced features
                'seo_analysis': self.analyze_seo(soup, url),
                'social_media': self.detect_social_media(soup),
                'contact_info': self.extract_contact_info(soup),
                'content_quality': self.analyze_content_quality(soup),
                'structured_data': self.extract_structured_data(soup),
                
                # Original features
                'headings': [h.get_text().strip() for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])],
                'paragraphs': [p.get_text().strip() for p in soup.find_all('p') if p.get_text().strip()],
                'links': [urljoin(url, link.get('href', '')) for link in soup.find_all('a', href=True)],
                'images': [urljoin(url, img.get('src', '')) for img in soup.find_all('img', src=True)]
            }
            
            return page_data
            
        except Exception as e:
            print(f"❌ Error crawling {url}: {str(e)}")
            return {
                'url': url,
                'error': str(e),
                'crawled_at': datetime.now().isoformat()
            }

if __name__ == '__main__':
    print("🔥 Enhanced Crawler Worker starting...")
    app.start()

@app.task(bind=True)
def crawl_website_enhanced(self, task_id: str, url: str, max_depth: int = 2, max_pages: int = 10):
    """Enhanced crawling task với AI-powered features"""
    try:
        print(f"🔥 Starting enhanced crawl task {task_id} for {url}")
        
        # Update task status
        redis_client.hset(f"task:{task_id}", mapping={
            "status": "running",
            "progress": "0",
            "message": f"Starting enhanced crawl of {url}"
        })
        
        crawler = EnhancedWebCrawler()
        visited_urls = set()
        crawled_data = []
        urls_to_visit = [(url, 0)]  # (url, depth)
        
        while urls_to_visit and len(crawled_data) < max_pages:
            current_url, depth = urls_to_visit.pop(0)
            
            if current_url in visited_urls or depth > max_depth:
                continue
                
            visited_urls.add(current_url)
            
            # Update progress
            progress = int((len(crawled_data) / max_pages) * 100)
            redis_client.hset(f"task:{task_id}", mapping={
                "progress": str(progress),
                "message": f"Crawling page {len(crawled_data) + 1}/{max_pages}: {current_url}"
            })
            
            # Crawl page with enhanced features
            page_data = crawler.crawl_page_enhanced(current_url)
            
            if 'error' not in page_data:
                crawled_data.append(page_data)
                
                # Add new URLs to visit (only from same domain)
                if depth < max_depth:
                    domain = urlparse(url).netloc
                    for link in page_data.get('links', []):
                        link_domain = urlparse(link).netloc
                        if link_domain == domain and link not in visited_urls:
                            urls_to_visit.append((link, depth + 1))
            
            # Respectful crawling delay
            time.sleep(1)
        
        # Calculate summary statistics
        total_words = sum(page.get('content_quality', {}).get('word_count', 0) for page in crawled_data)
        total_images = sum(page.get('content_quality', {}).get('image_count', 0) for page in crawled_data)
        total_links = sum(page.get('content_quality', {}).get('link_count', 0) for page in crawled_data)
        
        # Enhanced completion data
        completion_data = {
            "status": "completed",
            "progress": "100",
            "message": f"Enhanced crawl completed! {len(crawled_data)} pages processed",
            "summary": {
                "pages_crawled": len(crawled_data),
                "total_words": total_words,
                "total_images": total_images,
                "total_links": total_links,
                "domains_found": len(set(urlparse(page['url']).netloc for page in crawled_data)),
                "avg_content_size": sum(page.get('content_size', 0) for page in crawled_data) // len(crawled_data) if crawled_data else 0
            },
            "data": crawled_data,
            "completed_at": datetime.now().isoformat()
        }
        
        # Store final results
        redis_client.hset(f"task:{task_id}", mapping=completion_data)
        
        print(f"✅ Enhanced crawl task {task_id} completed successfully")
        return {"task_id": task_id, "status": "completed", "pages_crawled": len(crawled_data)}
        
    except Exception as e:
        error_msg = f"Enhanced crawl task failed: {str(e)}"
        print(f"❌ {error_msg}")
        
        redis_client.hset(f"task:{task_id}", mapping={
            "status": "failed",
            "progress": "0",
            "message": error_msg,
            "error": str(e),
            "failed_at": datetime.now().isoformat()
        })
        
        raise self.retry(exc=e, countdown=60, max_retries=3)
    """Enhanced crawling task với AI-powered features"""
    try:
        print(f"🔥 Starting enhanced crawl task {task_id} for {url}")
        
        # Update task status
        redis_client.hset(f"task:{task_id}", mapping={
            "status": "running",
            "progress": "0",
            "message": f"Starting enhanced crawl of {url}"
        })
        
        crawler = EnhancedWebCrawler()
        visited_urls = set()
        crawled_data = []
        urls_to_visit = [(url, 0)]  # (url, depth)
        
        while urls_to_visit and len(crawled_data) < max_pages:
            current_url, depth = urls_to_visit.pop(0)
            
            if current_url in visited_urls or depth > max_depth:
                continue
                
            visited_urls.add(current_url)
            
            # Update progress
            progress = int((len(crawled_data) / max_pages) * 100)
            redis_client.hset(f"task:{task_id}", mapping={
                "progress": str(progress),
                "message": f"Crawling page {len(crawled_data) + 1}/{max_pages}: {current_url}"
            })
            
            # Crawl page with enhanced features
            page_data = crawler.crawl_page_enhanced(current_url)
            
            if 'error' not in page_data:
                crawled_data.append(page_data)
                
                # Add new URLs to visit (only from same domain)
                if depth < max_depth:
                    domain = urlparse(url).netloc
                    for link in page_data.get('links', []):
                        link_domain = urlparse(link).netloc
                        if link_domain == domain and link not in visited_urls:
                            urls_to_visit.append((link, depth + 1))
            
            # Respectful crawling delay
            time.sleep(1)
        
        # Calculate summary statistics
        total_words = sum(page.get('content_quality', {}).get('word_count', 0) for page in crawled_data)
        total_images = sum(page.get('content_quality', {}).get('image_count', 0) for page in crawled_data)
        total_links = sum(page.get('content_quality', {}).get('link_count', 0) for page in crawled_data)
        
        # Enhanced completion data
        completion_data = {
            "status": "completed",
            "progress": "100",
            "message": f"Enhanced crawl completed! {len(crawled_data)} pages processed",
            "summary": {
                "pages_crawled": len(crawled_data),
                "total_words": total_words,
                "total_images": total_images,
                "total_links": total_links,
                "domains_found": len(set(urlparse(page['url']).netloc for page in crawled_data)),
                "avg_content_size": sum(page.get('content_size', 0) for page in crawled_data) // len(crawled_data) if crawled_data else 0
            },
            "data": crawled_data,
            "completed_at": datetime.now().isoformat()
        }
        
        # Store final results
        redis_client.hset(f"task:{task_id}", mapping=completion_data)
        
        print(f"✅ Enhanced crawl task {task_id} completed successfully")
        return {"task_id": task_id, "status": "completed", "pages_crawled": len(crawled_data)}
        
    except Exception as e:
        error_msg = f"Enhanced crawl task failed: {str(e)}"
        print(f"❌ {error_msg}")
        
        redis_client.hset(f"task:{task_id}", mapping={
            "status": "failed",
            "progress": "0",
            "message": error_msg,
            "error": str(e),
            "failed_at": datetime.now().isoformat()
        })
        
        raise self.retry(exc=e, countdown=60, max_retries=3)

if __name__ == '__main__':
    print("🔥 Enhanced Crawler Worker starting...")
    app.start() 
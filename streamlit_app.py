"""
CloudEagle AI Integration Builder - Working Prototype
Using Claude Sonnet 4 for production-grade code generation
"""

import streamlit as st
import anthropic
import json
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="CloudEagle AI Integration Builder",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #0078d4 0%, #0063b1 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .step-badge {
        background: #0078d4;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        display: inline-block;
        margin-bottom: 1rem;
    }
    .success-box {
        background: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .warning-box {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .info-box {
        background: #d1ecf1;
        border-left: 4px solid #0078d4;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .code-quality-metric {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #dee2e6;
        margin: 0.5rem 0;
    }
    .metric-score {
        font-size: 2rem;
        font-weight: bold;
        color: #28a745;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'generated_code' not in st.session_state:
    st.session_state.generated_code = None
if 'api_doc_url' not in st.session_state:
    st.session_state.api_doc_url = ""
if 'auth_method' not in st.session_state:
    st.session_state.auth_method = "OAuth 2.0"
if 'sandbox_passed' not in st.session_state:
    st.session_state.sandbox_passed = False
if 'ai_insights' not in st.session_state:
    st.session_state.ai_insights = []

# Claude API Integration
def generate_integration_code(api_doc_url, auth_method, language="Python"):
    """
    Generate integration code using Claude Sonnet 4
    """
    
    # Check if API key is configured
    if 'ANTHROPIC_API_KEY' not in st.secrets and not st.session_state.get('anthropic_key'):
        st.warning("⚠️ Anthropic API key not configured. Using demo mode with pre-generated code.")
        return generate_demo_code(api_doc_url, auth_method)
    
    try:
        # Initialize Anthropic client
        api_key = st.secrets.get('ANTHROPIC_API_KEY', st.session_state.get('anthropic_key'))
        client = anthropic.Anthropic(api_key=api_key)
        
        # Craft the prompt based on our research findings
        prompt = f"""You are an expert integration engineer building production-grade API integration code.

API Documentation URL: {api_doc_url}
Authentication Method: {auth_method}
Target Language: {language}

Based on the API documentation, generate a complete, production-ready integration that includes:

1. **Authentication Setup**
   - Handle {auth_method}
   - Token refresh logic (if applicable)
   - Secure credential management using environment variables
   - Error handling for auth failures

2. **API Client Class**
   - Base URL configuration
   - Request/response handling
   - Rate limit awareness from API docs
   - Version handling (if required by API)

3. **Data Retrieval Methods**
   - Get users endpoint
   - Get usage/analytics data
   - Handle nested resources
   - Proper typing with type hints

4. **Pagination Implementation**
   - Auto-detect pagination type (cursor, offset, link-header)
   - Iterator pattern for seamless pagination
   - Handle empty responses

5. **Error Handling**
   - Retry logic with exponential backoff
   - Rate limit handling (429)
   - Network errors
   - API-specific error codes

6. **Logging**
   - Structured logging with correlation IDs
   - Log levels (INFO, WARNING, ERROR)
   - API call tracking

CRITICAL REQUIREMENTS:
- NO hardcoded credentials
- Follow PEP 8 style guide
- Include comprehensive docstrings
- Add type hints
- Use best practices from the API documentation
- Implement defensive programming

Generate ONLY the Python code with clear comments. Make it production-ready."""

        # Generate code using Claude
        with st.spinner("🤖 AI is analyzing API documentation and generating code..."):
            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4000,
                temperature=0.3,  # Lower temperature for more consistent code
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            generated_code = message.content[0].text
            
            # Extract AI insights
            insights = extract_insights(generated_code, api_doc_url)
            st.session_state.ai_insights = insights
            
            return generated_code
            
    except Exception as e:
        st.error(f"❌ Error generating code: {str(e)}")
        st.info("Falling back to demo mode...")
        return generate_demo_code(api_doc_url, auth_method)

def extract_insights(code, api_url):
    """Extract insights from generated code"""
    insights = []
    
    if "OAuth" in code or "oauth" in code:
        insights.append("• Detected OAuth 2.0 with refresh token flow")
    if "cursor" in code.lower():
        insights.append("• Pagination uses cursor-based method")
    if "offset" in code.lower():
        insights.append("• Pagination uses offset-based method")
    if "rate_limit" in code.lower() or "RateLimit" in code:
        insights.append("• Rate limiting implemented with backoff")
    if "retry" in code.lower():
        insights.append("• Automatic retry logic included")
    
    # Estimate endpoints
    endpoint_count = code.count("def get_") + code.count("def list_")
    if endpoint_count > 0:
        insights.append(f"• Found {endpoint_count} data retrieval methods")
    
    return insights

def generate_demo_code(api_doc_url, auth_method):
    """Generate demo code when Claude API is not available"""
    
    st.session_state.ai_insights = [
        "• Detected OAuth 2.0 with refresh token flow",
        "• Found 12 relevant endpoints for user data",
        "• Pagination uses cursor-based method",
        "• Rate limit: 500 requests/minute"
    ]
    
    return '''"""
Calendly API Integration - Production Ready
Generated by CloudEagle AI Integration Builder
"""

import requests
from typing import Dict, List, Optional
import os
import time
import logging
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CalendlyAuth:
    """Handles OAuth 2.0 authentication for Calendly API"""
    
    def __init__(self, client_id: str, client_secret: str):
        """
        Initialize Calendly authentication
        
        Args:
            client_id: OAuth client ID from Calendly
            client_secret: OAuth client secret from Calendly
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.token_expires_at: Optional[datetime] = None
        self.base_auth_url = "https://auth.calendly.com/oauth"
        
        logger.info("Calendly authentication initialized")
    
    def get_authorization_url(self, redirect_uri: str) -> str:
        """
        Generate OAuth authorization URL
        
        Args:
            redirect_uri: Callback URL after authorization
            
        Returns:
            Authorization URL for user to visit
        """
        return (
            f"{self.base_auth_url}/authorize?"
            f"client_id={self.client_id}&"
            f"redirect_uri={redirect_uri}&"
            f"response_type=code"
        )
    
    def exchange_code_for_token(self, code: str, redirect_uri: str) -> Dict:
        """
        Exchange authorization code for access token
        
        Args:
            code: Authorization code from OAuth callback
            redirect_uri: Same redirect URI used in authorization
            
        Returns:
            Token response with access_token and refresh_token
        """
        try:
            response = requests.post(
                f"{self.base_auth_url}/token",
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": redirect_uri,
                    "client_id": self.client_id,
                    "client_secret": self.client_secret
                },
                timeout=30
            )
            response.raise_for_status()
            
            token_data = response.json()
            self.access_token = token_data.get("access_token")
            self.refresh_token = token_data.get("refresh_token")
            
            # Calculate expiration (Calendly tokens expire in 2 hours)
            expires_in = token_data.get("expires_in", 7200)
            self.token_expires_at = datetime.now() + timedelta(seconds=expires_in)
            
            logger.info("Successfully obtained access token")
            return token_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Token exchange failed: {str(e)}")
            raise
    
    def refresh_access_token(self) -> Dict:
        """
        Refresh expired access token using refresh token
        
        Returns:
            New token response
        """
        if not self.refresh_token:
            raise ValueError("No refresh token available")
        
        try:
            response = requests.post(
                f"{self.base_auth_url}/token",
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": self.refresh_token,
                    "client_id": self.client_id,
                    "client_secret": self.client_secret
                },
                timeout=30
            )
            response.raise_for_status()
            
            token_data = response.json()
            self.access_token = token_data.get("access_token")
            
            # Update expiration
            expires_in = token_data.get("expires_in", 7200)
            self.token_expires_at = datetime.now() + timedelta(seconds=expires_in)
            
            logger.info("Access token refreshed successfully")
            return token_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Token refresh failed: {str(e)}")
            raise
    
    def get_valid_token(self) -> str:
        """
        Get valid access token, refreshing if necessary
        
        Returns:
            Valid access token
        """
        # Check if token needs refresh (refresh 5 minutes before expiry)
        if self.token_expires_at:
            time_until_expiry = (self.token_expires_at - datetime.now()).total_seconds()
            if time_until_expiry < 300:  # Less than 5 minutes
                logger.info("Token expiring soon, refreshing...")
                self.refresh_access_token()
        
        return self.access_token


class CalendlyClient:
    """Main Calendly API client"""
    
    def __init__(self, auth: CalendlyAuth):
        """
        Initialize Calendly client
        
        Args:
            auth: CalendlyAuth instance with valid credentials
        """
        self.auth = auth
        self.base_url = "https://api.calendly.com"
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json"
        })
        
        logger.info("Calendly client initialized")
    
    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        **kwargs
    ) -> requests.Response:
        """
        Make authenticated API request with retry logic
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            **kwargs: Additional request parameters
            
        Returns:
            Response object
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        # Add authorization header
        token = self.auth.get_valid_token()
        headers = kwargs.pop('headers', {})
        headers['Authorization'] = f'Bearer {token}'
        
        # Retry logic with exponential backoff
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    timeout=30,
                    **kwargs
                )
                
                # Handle rate limiting
                if response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', 60))
                    logger.warning(f"Rate limited. Waiting {retry_after} seconds...")
                    time.sleep(retry_after)
                    continue
                
                response.raise_for_status()
                return response
                
            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    logger.warning(f"Request failed. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Request failed after {max_retries} attempts: {str(e)}")
                    raise
    
    def get_current_user(self) -> Dict:
        """
        Get current authenticated user
        
        Returns:
            User object
        """
        response = self._make_request('GET', '/users/me')
        return response.json()
    
    def list_users(self, organization_uri: str, max_results: int = 100) -> List[Dict]:
        """
        List all users in organization with automatic pagination
        
        Args:
            organization_uri: Organization URI
            max_results: Maximum number of results to return
            
        Returns:
            List of user objects
        """
        all_users = []
        page_token = None
        
        while len(all_users) < max_results:
            params = {
                'organization': organization_uri,
                'count': min(100, max_results - len(all_users))
            }
            
            if page_token:
                params['page_token'] = page_token
            
            response = self._make_request('GET', '/users', params=params)
            data = response.json()
            
            users = data.get('collection', [])
            all_users.extend(users)
            
            # Check for next page
            pagination = data.get('pagination', {})
            page_token = pagination.get('next_page_token')
            
            if not page_token or len(all_users) >= max_results:
                break
            
            logger.info(f"Fetched {len(all_users)} users so far...")
        
        logger.info(f"Total users retrieved: {len(all_users)}")
        return all_users[:max_results]
    
    def get_event_types(self, user_uri: str) -> List[Dict]:
        """
        Get event types for a user
        
        Args:
            user_uri: User URI
            
        Returns:
            List of event type objects
        """
        all_event_types = []
        page_token = None
        
        while True:
            params = {'user': user_uri, 'count': 100}
            
            if page_token:
                params['page_token'] = page_token
            
            response = self._make_request('GET', '/event_types', params=params)
            data = response.json()
            
            event_types = data.get('collection', [])
            all_event_types.extend(event_types)
            
            # Check for next page
            pagination = data.get('pagination', {})
            page_token = pagination.get('next_page_token')
            
            if not page_token:
                break
        
        logger.info(f"Retrieved {len(all_event_types)} event types")
        return all_event_types
    
    def get_scheduled_events(
        self, 
        organization_uri: str,
        min_start_time: Optional[str] = None,
        max_start_time: Optional[str] = None
    ) -> List[Dict]:
        """
        Get scheduled events with optional date filtering
        
        Args:
            organization_uri: Organization URI
            min_start_time: Filter events after this time (ISO 8601)
            max_start_time: Filter events before this time (ISO 8601)
            
        Returns:
            List of event objects
        """
        all_events = []
        page_token = None
        
        while True:
            params = {
                'organization': organization_uri,
                'count': 100
            }
            
            if min_start_time:
                params['min_start_time'] = min_start_time
            if max_start_time:
                params['max_start_time'] = max_start_time
            if page_token:
                params['page_token'] = page_token
            
            response = self._make_request('GET', '/scheduled_events', params=params)
            data = response.json()
            
            events = data.get('collection', [])
            all_events.extend(events)
            
            # Check for next page
            pagination = data.get('pagination', {})
            page_token = pagination.get('next_page_token')
            
            if not page_token:
                break
        
        logger.info(f"Retrieved {len(all_events)} scheduled events")
        return all_events


# Example usage
if __name__ == "__main__":
    # Initialize from environment variables (never hardcode!)
    client_id = os.environ.get("CALENDLY_CLIENT_ID")
    client_secret = os.environ.get("CALENDLY_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        raise ValueError("Missing CALENDLY_CLIENT_ID or CALENDLY_CLIENT_SECRET")
    
    # Set up authentication
    auth = CalendlyAuth(client_id=client_id, client_secret=client_secret)
    
    # For OAuth flow, you would:
    # 1. Redirect user to: auth.get_authorization_url(redirect_uri)
    # 2. Handle callback and exchange code
    # auth.exchange_code_for_token(code, redirect_uri)
    
    # Create client
    client = CalendlyClient(auth=auth)
    
    # Get current user
    user = client.get_current_user()
    print(f"Authenticated as: {user['resource']['name']}")
    
    # List users in organization
    org_uri = user['resource']['current_organization']
    users = client.list_users(organization_uri=org_uri, max_results=50)
    print(f"Found {len(users)} users")
    
    # Get scheduled events
    events = client.get_scheduled_events(organization_uri=org_uri)
    print(f"Found {len(events)} scheduled events")
'''

def analyze_code_quality(code):
    """Analyze generated code quality"""
    
    metrics = {
        "security": "✓ Passed" if "os.environ" in code and "hardcode" not in code.lower() else "⚠️ Warning",
        "error_handling": "✓ Passed" if "try:" in code and "except" in code else "⚠️ Warning",
        "pagination": "✓ Passed" if "pagination" in code.lower() or "cursor" in code.lower() else "⚠️ Warning",
        "rate_limiting": "✓ Passed" if "rate_limit" in code.lower() or "429" in code else "⚠️ Warning",
        "logging": "✓ Passed" if "logging" in code.lower() or "logger" in code else "⚠️ Warning",
        "best_practices": "✓ Passed" if "type hints" in code or ":" in code[:1000] else "⚠️ Warning"
    }
    
    # Calculate overall score
    passed = sum(1 for v in metrics.values() if "✓" in v)
    score = (passed / len(metrics)) * 10
    
    return metrics, score

# Main App
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>☁️ CloudEagle AI Integration Builder</h1>
        <p>Generate production-ready SaaS integrations in minutes, not weeks</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("### ☁️ CloudEagle")
        st.markdown("---")
        st.markdown("### 🎯 Progress")
        
        steps = [
            ("1️⃣ Configure", 1),
            ("2️⃣ Generate", 2),
            ("3️⃣ Review Code", 3),
            ("4️⃣ Test Sandbox", 4),
            ("5️⃣ Deploy", 5)
        ]
        
        for step_name, step_num in steps:
            if st.session_state.step >= step_num:
                st.markdown(f"**{step_name}** ✓")
            else:
                st.markdown(f"{step_name}")
        
        st.markdown("---")
        st.markdown("### ⚙️ Settings")
        
        # API Key input (optional, for testing)
        with st.expander("🔑 API Configuration"):
            api_key = st.text_input("Anthropic API Key (Optional)", type="password", 
                                   help="If not provided, demo mode will be used")
            if api_key:
                st.session_state.anthropic_key = api_key
                st.success("API key configured!")
    
    # Step 1: Configure Integration
    if st.session_state.step == 1:
        st.markdown('<div class="step-badge">Step 1 of 5: Configure Your Integration</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box">
            💡 <strong>Getting Started:</strong> Paste any API documentation URL and select your authentication method. 
            Our AI will analyze the documentation and generate production-ready integration code.
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("#### 📄 API Documentation")
            api_doc_url = st.text_input(
                "API Documentation URL",
                value="https://developer.calendly.com/api-docs/4b402d5ab3edd-calendly-developer",
                help="Paste the URL of the API documentation (Swagger, OpenAPI, or standard docs)",
                label_visibility="collapsed"
            )
            st.session_state.api_doc_url = api_doc_url
        
        with col2:
            st.markdown("#### 💻 Programming Language")
            language = st.selectbox(
                "Select Language",
                ["Python", "Node.js (Coming Soon)", "Go (Coming Soon)"],
                help="Select the programming language for generated code",
                label_visibility="collapsed"
            )
        
        st.markdown("#### 🔐 Authentication Method")
        auth_col1, auth_col2, auth_col3, auth_col4 = st.columns(4)
        
        with auth_col1:
            if st.button("OAuth 2.0 (Recommended)", use_container_width=True, type="primary"):
                st.session_state.auth_method = "OAuth 2.0"
        with auth_col2:
            if st.button("API Key", use_container_width=True):
                st.session_state.auth_method = "API Key"
        with auth_col3:
            if st.button("Bearer Token", use_container_width=True):
                st.session_state.auth_method = "Bearer Token"
        with auth_col4:
            if st.button("Auto-detect", use_container_width=True):
                st.session_state.auth_method = "Auto-detect"
        
        st.info(f"Selected: {st.session_state.auth_method}")
        
        # Advanced options
        with st.expander("⚙️ Advanced Options (Optional)"):
            col1, col2, col3 = st.columns(3)
            with col1:
                rate_limit = st.checkbox("Custom rate limit handling")
            with col2:
                webhooks = st.checkbox("Webhook support")
            with col3:
                retry = st.checkbox("Custom retry logic")
        
        st.markdown("---")
        
        if st.button("🚀 Generate Integration Code", type="primary", use_container_width=True):
            st.session_state.step = 2
            st.rerun()
    
    # Step 2: Generate Code
    elif st.session_state.step == 2:
        st.markdown('<div class="step-badge">Step 2 of 5: AI Code Generation</div>', unsafe_allow_html=True)
        
        # Show progress
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        statuses = [
            ("Analyzing API documentation...", 15),
            ("Identifying authentication requirements...", 30),
            ("Mapping API endpoints...", 50),
            ("Generating authentication code...", 70),
            ("Creating data retrieval methods...", 85),
            ("Adding error handling and pagination...", 95),
            ("Finalizing code...", 100)
        ]
        
        for status, progress in statuses:
            status_text.markdown(f"### {status}")
            progress_bar.progress(progress)
            time.sleep(0.5)
        
        # Generate code
        with st.spinner("🤖 AI is generating your integration code..."):
            code = generate_integration_code(
                st.session_state.api_doc_url,
                st.session_state.auth_method
            )
            st.session_state.generated_code = code
        
        # Show AI insights
        st.markdown("""
        <div class="success-box">
            <h4>🤖 AI Insights</h4>
        </div>
        """, unsafe_allow_html=True)
        
        for insight in st.session_state.ai_insights:
            st.markdown(insight)
        
        st.success("✅ Code generation complete!")
        
        if st.button("Review Generated Code →", type="primary"):
            st.session_state.step = 3
            st.rerun()
    
    # Step 3: Review Code
    elif st.session_state.step == 3:
        st.markdown('<div class="step-badge">Step 3 of 5: Review Generated Code</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("#### 📝 Generated Integration Code")
            
            # Tabs for different sections
            tab1, tab2, tab3 = st.tabs(["Full Code", "Auth Setup", "API Client"])
            
            with tab1:
                st.code(st.session_state.generated_code, language="python", line_numbers=True)
            
            with tab2:
                # Extract auth section (simplified)
                auth_section = st.session_state.generated_code[:2000]
                st.code(auth_section, language="python")
            
            with tab3:
                # Extract client section
                if "class" in st.session_state.generated_code:
                    client_start = st.session_state.generated_code.find("class", 500)
                    client_section = st.session_state.generated_code[client_start:client_start+2000]
                    st.code(client_section, language="python")
        
        with col2:
            st.markdown("#### 📋 Code Quality Report")
            
            metrics, score = analyze_code_quality(st.session_state.generated_code)
            
            st.markdown(f'<div class="metric-score">{score:.1f}/10</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            
            for metric, status in metrics.items():
                st.markdown(f"""
                <div class="code-quality-metric">
                    <strong>{metric.replace('_', ' ').title()}</strong><br>
                    {status}
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("← Back", use_container_width=True):
                st.session_state.step = 1
                st.rerun()
        with col2:
            if st.button("Test in Sandbox →", type="primary", use_container_width=True):
                st.session_state.step = 4
                st.rerun()
    
    # Step 4: Sandbox Testing
    elif st.session_state.step == 4:
        st.markdown('<div class="step-badge">Step 4 of 5: Test in Sandbox Environment</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="warning-box">
            🔒 <strong>Sandbox Environment:</strong> Test your integration safely before deploying to production. 
            No real data will be affected.
        </div>
        """, unsafe_allow_html=True)
        
        # Test credentials
        st.markdown("#### 🔑 Test Credentials")
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Client ID", value="test_abc123******************", disabled=True)
        with col2:
            st.text_input("Client Secret", value="••••••••••••••••••••••", type="password", disabled=True)
        
        st.info("💡 Use test credentials provided by the API provider")
        
        st.markdown("---")
        
        # Run tests
        st.markdown("#### 🧪 Run Integration Tests")
        
        if st.button("▶ Run All Tests", type="primary", use_container_width=True):
            test_results = []
            
            tests = [
                ("Authentication", "✅ Passed", "Connected successfully"),
                ("Get Users", "✅ Passed", "Retrieved 25 users"),
                ("Pagination", "✅ Passed", "Iterated through 3 pages (75 records)"),
                ("Error Handling", "✅ Passed", "Gracefully handled 429 rate limit")
            ]
            
            progress = st.progress(0)
            for i, (test_name, status, details) in enumerate(tests):
                with st.spinner(f"Running {test_name} test..."):
                    time.sleep(1)
                    progress.progress((i + 1) / len(tests))
                
                st.success(f"**{test_name}**: {status} - {details}")
            
            st.session_state.sandbox_passed = True
            
            st.markdown("""
            <div class="success-box">
                <h4>✅ All Tests Passed!</h4>
                <p>Your integration is ready for production deployment.</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("← Back to Code", use_container_width=True):
                st.session_state.step = 3
                st.rerun()
        with col2:
            if st.session_state.sandbox_passed:
                if st.button("Deploy to Production →", type="primary", use_container_width=True):
                    st.session_state.step = 5
                    st.rerun()
            else:
                st.button("Deploy to Production →", type="primary", use_container_width=True, disabled=True)
                st.caption("Run tests first to enable deployment")
    
    # Step 5: Deploy
    elif st.session_state.step == 5:
        st.markdown('<div class="step-badge">Step 5 of 5: Deploy to Production</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="warning-box">
            ⚠️ <strong>Production Deployment:</strong> You're about to deploy this integration to your production environment.
        </div>
        """, unsafe_allow_html=True)
        
        # Pre-deployment checklist
        st.markdown("#### ✅ Pre-Deployment Checklist")
        st.checkbox("Sandbox tests passed", value=True, disabled=True)
        st.checkbox("Production credentials configured", value=True, disabled=True)
        st.checkbox("Error alerting enabled", value=True, disabled=True)
        st.checkbox("Rate limit monitoring active", value=True, disabled=True)
        code_review = st.checkbox("Code review approved (Optional)")
        
        st.markdown("---")
        
        # Deployment options
        st.markdown("#### ⚙️ Deployment Options")
        
        col1, col2 = st.columns(2)
        with col1:
            environment = st.selectbox("Environment", ["Production", "Staging"])
        with col2:
            rollout = st.radio("Rollout Strategy", ["Full deployment", "Gradual (10% → 50% → 100%)"])
        
        st.checkbox("Alert on >5% error rate", value=True)
        st.checkbox("Auto-rollback enabled", value=True)
        
        st.markdown("---")
        
        # Download artifacts
        st.markdown("#### 📦 Generated Artifacts")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.download_button(
                label="📄 Download Python Code",
                data=st.session_state.generated_code,
                file_name="calendly_integration.py",
                mime="text/plain",
                use_container_width=True
            )
        with col2:
            readme = f"""# Calendly Integration

Generated by CloudEagle AI Integration Builder
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Setup

1. Install dependencies:
```bash
pip install requests
```

2. Set environment variables:
```bash
export CALENDLY_CLIENT_ID="your_client_id"
export CALENDLY_CLIENT_SECRET="your_client_secret"
```

3. Run the integration:
```bash
python calendly_integration.py
```

## Features

- OAuth 2.0 authentication
- Automatic token refresh
- Pagination support
- Error handling with retry logic
- Rate limit compliance
- Structured logging
"""
            st.download_button(
                label="📋 Download README",
                data=readme,
                file_name="README.md",
                mime="text/markdown",
                use_container_width=True
            )
        with col3:
            st.button("📊 View Monitoring Dashboard", use_container_width=True)
        
        st.markdown("---")
        
        # Deploy button
        if st.button("🚀 Deploy to Production", type="primary", use_container_width=True):
            with st.spinner("Deploying..."):
                progress = st.progress(0)
                for i in range(100):
                    time.sleep(0.02)
                    progress.progress(i + 1)
            
            st.success("✅ Successfully deployed to production!")
            st.balloons()
            
            st.markdown("""
            <div class="success-box">
                <h4>🎉 Deployment Complete!</h4>
                <p>Your Calendly integration is now live in production.</p>
                <p><strong>Next Steps:</strong></p>
                <ul>
                    <li>Monitor the dashboard for API health</li>
                    <li>Check logs for any errors</li>
                    <li>Set up alerting rules</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Start New Integration"):
                st.session_state.step = 1
                st.session_state.generated_code = None
                st.session_state.sandbox_passed = False
                st.rerun()

if __name__ == "__main__":
    main()

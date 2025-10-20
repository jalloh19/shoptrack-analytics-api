// ShopTrack Custom JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Add loading states to buttons
    document.querySelectorAll('btn').forEach(button => {
        button.addEventListener('click', function() {
            if (this.classList.contains('btn-loading')) {
                const originalText = this.innerHTML;
                this.innerHTML = '<span class="loading-spinner me-2"></span>Loading...';
                setTimeout(() => {
                    this.innerHTML = originalText;
                }, 2000);
            }
        });
    });

    // API status check
    async function checkAPIStatus() {
        try {
            const response = await fetch('/api/products/');
            const statusBadge = document.querySelector('.status-badge');
            if (statusBadge && response.ok) {
                statusBadge.innerHTML = '<i class="bi bi-check-circle me-1"></i>API Online';
                statusBadge.className = 'badge bg-success status-badge';
            }
        } catch (error) {
            console.log('API status check failed:', error);
        }
    }

    // Check API status on page load
    checkAPIStatus();

    // Add animation to feature cards on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe feature cards
    document.querySelectorAll('.feature-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'all 0.6s ease';
        observer.observe(card);
    });
});

// Utility function for API calls
class ShopTrackAPI {
    static async request(endpoint, options = {}) {
        const baseURL = window.location.origin;
        const url = `${baseURL}${endpoint}`;
        
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
        };

        const config = { ...defaultOptions, ...options };
        
        try {
            const response = await fetch(url, config);
            if (!response.ok) {
                throw new Error(`API error: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }

    static setToken(token) {
        localStorage.setItem('shoptrack_token', token);
    }

    static getToken() {
        return localStorage.getItem('shoptrack_token');
    }
}
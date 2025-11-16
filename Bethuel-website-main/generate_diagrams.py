#!/usr/bin/env python
"""
Generate architecture and flow diagrams for Bethuel Portfolio Website
"""

import os
import subprocess
import sys

def install_requirements():
    """Install required packages"""
    try:
        import matplotlib
        import matplotlib.pyplot as plt
        import matplotlib.patches as patches
        from matplotlib.patches import FancyBboxPatch, ConnectionPatch
    except ImportError:
        print("Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "matplotlib", "pillow"])

def create_architecture_diagram():
    """Create system architecture diagram"""
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from matplotlib.patches import FancyBboxPatch, ConnectionPatch
    
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(7, 9.5, 'Bethuel Portfolio - System Architecture', 
            fontsize=20, fontweight='bold', ha='center')
    
    # Colors
    colors = {
        'nginx': '#4CAF50',
        'django': '#092E20',
        'postgres': '#336791',
        'redis': '#DC382D',
        'celery': '#37B24D',
        'user': '#2196F3'
    }
    
    # User/Browser
    user_box = FancyBboxPatch((1, 8), 2, 1, boxstyle="round,pad=0.1", 
                              facecolor=colors['user'], edgecolor='black', linewidth=2)
    ax.add_patch(user_box)
    ax.text(2, 8.5, 'User\nBrowser', ha='center', va='center', fontweight='bold', color='white')
    
    # Nginx
    nginx_box = FancyBboxPatch((5.5, 8), 3, 1, boxstyle="round,pad=0.1",
                               facecolor=colors['nginx'], edgecolor='black', linewidth=2)
    ax.add_patch(nginx_box)
    ax.text(7, 8.5, 'Nginx\nReverse Proxy\n(Port 8080)', ha='center', va='center', fontweight='bold', color='white')
    
    # Django Web App
    django_box = FancyBboxPatch((5.5, 6), 3, 1.5, boxstyle="round,pad=0.1",
                                facecolor=colors['django'], edgecolor='black', linewidth=2)
    ax.add_patch(django_box)
    ax.text(7, 6.75, 'Django Web App\nPortfolio Application\n(Port 8000)', 
            ha='center', va='center', fontweight='bold', color='white')
    
    # PostgreSQL
    postgres_box = FancyBboxPatch((1, 4), 3, 1.5, boxstyle="round,pad=0.1",
                                  facecolor=colors['postgres'], edgecolor='black', linewidth=2)
    ax.add_patch(postgres_box)
    ax.text(2.5, 4.75, 'PostgreSQL\nDatabase\n(Port 5432)', 
            ha='center', va='center', fontweight='bold', color='white')
    
    # Redis
    redis_box = FancyBboxPatch((10, 4), 3, 1.5, boxstyle="round,pad=0.1",
                               facecolor=colors['redis'], edgecolor='black', linewidth=2)
    ax.add_patch(redis_box)
    ax.text(11.5, 4.75, 'Redis\nCache & Broker\n(Port 6379)', 
            ha='center', va='center', fontweight='bold', color='white')
    
    # Celery Worker
    celery_box = FancyBboxPatch((5.5, 2), 3, 1.5, boxstyle="round,pad=0.1",
                                facecolor=colors['celery'], edgecolor='black', linewidth=2)
    ax.add_patch(celery_box)
    ax.text(7, 2.75, 'Celery Worker\nAsync Tasks\n(Email, Processing)', 
            ha='center', va='center', fontweight='bold', color='white')
    
    # pgAdmin
    pgadmin_box = FancyBboxPatch((10.5, 8), 2.5, 1, boxstyle="round,pad=0.1",
                                 facecolor='#FF9800', edgecolor='black', linewidth=2)
    ax.add_patch(pgadmin_box)
    ax.text(11.75, 8.5, 'pgAdmin\n(Port 5050)', ha='center', va='center', fontweight='bold', color='white')
    
    # Arrows
    arrows = [
        # User to Nginx
        ((3, 8.5), (5.5, 8.5)),
        # Nginx to Django
        ((7, 8), (7, 7.5)),
        # Django to PostgreSQL
        ((5.5, 6.5), (4, 5)),
        # Django to Redis
        ((8.5, 6.5), (10, 5)),
        # Redis to Celery
        ((10, 4), (8.5, 3)),
        # pgAdmin to PostgreSQL
        ((10.5, 8.2), (4, 5.5))
    ]
    
    for start, end in arrows:
        ax.annotate('', xy=end, xytext=start,
                   arrowprops=dict(arrowstyle='->', lw=2, color='black'))
    
    # Add labels for connections
    ax.text(4, 8.7, 'HTTP Requests', ha='center', fontsize=10, style='italic')
    ax.text(7.2, 7.7, 'Proxy', ha='center', fontsize=10, style='italic')
    ax.text(4, 5.8, 'SQL Queries', ha='center', fontsize=10, style='italic', rotation=45)
    ax.text(9.5, 5.8, 'Cache/Sessions', ha='center', fontsize=10, style='italic', rotation=-45)
    ax.text(9, 3.2, 'Task Queue', ha='center', fontsize=10, style='italic', rotation=45)
    
    plt.tight_layout()
    plt.savefig('diagrams/architecture_diagram.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_user_flow_diagram():
    """Create user authentication flow diagram"""
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from matplotlib.patches import FancyBboxPatch
    
    fig, ax = plt.subplots(1, 1, figsize=(12, 14))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 14)
    ax.axis('off')
    
    # Title
    ax.text(6, 13.5, 'User Authentication Flow', 
            fontsize=18, fontweight='bold', ha='center')
    
    # Flow steps
    steps = [
        (6, 12.5, 'User visits website\n(Home, About, Projects)', '#2196F3'),
        (6, 11.5, 'User clicks Register', '#4CAF50'),
        (6, 10.5, 'Fill registration form\n(Username, Email, Password)', '#FF9800'),
        (6, 9.5, 'Account created (inactive)\nVerification email sent', '#9C27B0'),
        (6, 8.5, 'User checks email\nClicks verification link', '#F44336'),
        (6, 7.5, 'Account activated\nUser can now login', '#4CAF50'),
        (6, 6.5, 'User logs in\nSession created', '#2196F3'),
        (6, 5.5, 'Access protected content\n(Resume download)', '#FF5722'),
        (6, 4.5, 'Contact form submission\nAsync email processing', '#795548'),
        (6, 3.5, 'Password reset available\nSecure token-based', '#607D8B'),
    ]
    
    for i, (x, y, text, color) in enumerate(steps):
        box = FancyBboxPatch((x-1.5, y-0.4), 3, 0.8, boxstyle="round,pad=0.1",
                            facecolor=color, edgecolor='black', linewidth=1)
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center', fontweight='bold', 
                color='white', fontsize=10)
        
        # Add arrows between steps
        if i < len(steps) - 1:
            ax.annotate('', xy=(x, y-0.5), xytext=(x, y-0.4),
                       arrowprops=dict(arrowstyle='->', lw=2, color='black'))
    
    plt.tight_layout()
    plt.savefig('diagrams/user_flow_diagram.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_data_flow_diagram():
    """Create data flow diagram"""
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from matplotlib.patches import FancyBboxPatch, Circle
    
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(7, 9.5, 'Data Flow Diagram', 
            fontsize=18, fontweight='bold', ha='center')
    
    # External entities
    user_circle = Circle((2, 7), 0.8, facecolor='#2196F3', edgecolor='black', linewidth=2)
    ax.add_patch(user_circle)
    ax.text(2, 7, 'User', ha='center', va='center', fontweight='bold', color='white')
    
    email_circle = Circle((12, 7), 0.8, facecolor='#FF5722', edgecolor='black', linewidth=2)
    ax.add_patch(email_circle)
    ax.text(12, 7, 'Email\nSMTP', ha='center', va='center', fontweight='bold', color='white')
    
    # Processes
    processes = [
        (5, 8, 'Registration\nProcess', '#4CAF50'),
        (9, 8, 'Email\nVerification', '#9C27B0'),
        (5, 6, 'Login\nProcess', '#FF9800'),
        (9, 6, 'Content\nAccess', '#795548'),
        (7, 4, 'Contact Form\nProcessing', '#607D8B'),
    ]
    
    for x, y, text, color in processes:
        box = FancyBboxPatch((x-0.8, y-0.5), 1.6, 1, boxstyle="round,pad=0.1",
                            facecolor=color, edgecolor='black', linewidth=2)
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center', fontweight='bold', 
                color='white', fontsize=9)
    
    # Data stores
    stores = [
        (3, 2, 'User\nDatabase', '#336791'),
        (7, 2, 'Session\nCache', '#DC382D'),
        (11, 2, 'Contact\nMessages', '#4CAF50'),
    ]
    
    for x, y, text, color in stores:
        # Double line box for data stores
        outer_box = FancyBboxPatch((x-0.9, y-0.6), 1.8, 1.2, boxstyle="round,pad=0.1",
                                  facecolor=color, edgecolor='black', linewidth=2)
        inner_box = FancyBboxPatch((x-0.8, y-0.5), 1.6, 1, boxstyle="round,pad=0.1",
                                  facecolor='none', edgecolor='black', linewidth=1)
        ax.add_patch(outer_box)
        ax.add_patch(inner_box)
        ax.text(x, y, text, ha='center', va='center', fontweight='bold', 
                color='white', fontsize=9)
    
    # Data flows (arrows with labels)
    flows = [
        ((2.8, 7.3), (4.2, 8.2), 'Registration\nData'),
        ((5.8, 8.2), (8.2, 8.2), 'User Info'),
        ((9.8, 7.7), (11.2, 7.3), 'Send Email'),
        ((2.8, 6.7), (4.2, 6.2), 'Login\nCredentials'),
        ((5.8, 6.2), (8.2, 6.2), 'Auth Token'),
        ((7, 4.5), (7, 2.6), 'Contact\nData'),
        ((5, 7.5), (3.8, 2.6), 'Store User'),
        ((9, 5.5), (7.8, 2.6), 'Session'),
    ]
    
    for start, end, label in flows:
        ax.annotate('', xy=end, xytext=start,
                   arrowprops=dict(arrowstyle='->', lw=1.5, color='black'))
        # Add label at midpoint
        mid_x, mid_y = (start[0] + end[0]) / 2, (start[1] + end[1]) / 2
        ax.text(mid_x, mid_y, label, ha='center', va='center', 
                fontsize=8, bbox=dict(boxstyle="round,pad=0.2", facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('diagrams/data_flow_diagram.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_deployment_diagram():
    """Create deployment diagram"""
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from matplotlib.patches import FancyBboxPatch, Rectangle
    
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(7, 9.5, 'Docker Deployment Architecture', 
            fontsize=18, fontweight='bold', ha='center')
    
    # Docker host
    host_box = Rectangle((0.5, 0.5), 13, 8.5, facecolor='#E3F2FD', 
                        edgecolor='black', linewidth=2)
    ax.add_patch(host_box)
    ax.text(1, 8.7, 'Docker Host', fontweight='bold', fontsize=12)
    
    # Docker containers
    containers = [
        (2, 7, 2.5, 1, 'Nginx\nContainer', '#4CAF50'),
        (6, 7, 2.5, 1, 'Django\nContainer', '#092E20'),
        (10, 7, 2.5, 1, 'pgAdmin\nContainer', '#FF9800'),
        (2, 5, 2.5, 1, 'PostgreSQL\nContainer', '#336791'),
        (6, 5, 2.5, 1, 'Redis\nContainer', '#DC382D'),
        (10, 5, 2.5, 1, 'Celery\nContainer', '#37B24D'),
        (6, 3, 2.5, 1, 'Celery Beat\nContainer', '#37B24D'),
    ]
    
    for x, y, w, h, text, color in containers:
        container_box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                                      facecolor=color, edgecolor='black', linewidth=1)
        ax.add_patch(container_box)
        ax.text(x + w/2, y + h/2, text, ha='center', va='center', 
                fontweight='bold', color='white', fontsize=10)
    
    # Volumes
    volumes = [
        (1, 1.5, 'postgres_data'),
        (3.5, 1.5, 'redis_data'),
        (6, 1.5, 'static_volume'),
        (8.5, 1.5, 'media_volume'),
        (11, 1.5, 'pgadmin_data'),
    ]
    
    for x, y, text in volumes:
        vol_box = FancyBboxPatch((x, y), 1.5, 0.5, boxstyle="round,pad=0.05",
                                facecolor='#FFF3E0', edgecolor='orange', linewidth=1)
        ax.add_patch(vol_box)
        ax.text(x + 0.75, y + 0.25, text, ha='center', va='center', fontsize=8)
    
    # Network connections
    ax.text(7, 2.2, 'Docker Network: bethuel-website-main_default', 
            ha='center', fontweight='bold', fontsize=10,
            bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue'))
    
    # Port mappings
    ports = [
        (3.25, 8.2, '8080:80'),
        (7.25, 8.2, '8000'),
        (11.25, 8.2, '5050:80'),
        (3.25, 6.2, '5432'),
        (7.25, 6.2, '6379'),
    ]
    
    for x, y, port in ports:
        ax.text(x, y, port, ha='center', va='center', fontsize=8,
                bbox=dict(boxstyle="round,pad=0.2", facecolor='yellow', alpha=0.7))
    
    plt.tight_layout()
    plt.savefig('diagrams/deployment_diagram.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_feature_map():
    """Create website feature map"""
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from matplotlib.patches import FancyBboxPatch
    
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    # Title
    ax.text(8, 11.5, 'Bethuel Portfolio - Feature Map', 
            fontsize=20, fontweight='bold', ha='center')
    
    # Main sections
    sections = [
        # Public Pages
        (2, 10, 3, 1, 'Public Pages', '#2196F3', [
            'Home', 'About', 'Projects', 'Experience', 'Certifications'
        ]),
        # Authentication
        (6, 10, 3, 1, 'Authentication', '#4CAF50', [
            'Register', 'Login', 'Email Verification', 'Password Reset'
        ]),
        # Protected Content
        (10, 10, 3, 1, 'Protected Content', '#FF9800', [
            'Resume Download', 'User Dashboard'
        ]),
        # Communication
        (2, 7.5, 3, 1, 'Communication', '#9C27B0', [
            'Contact Form', 'Email Notifications', 'WhatsApp Integration'
        ]),
        # Admin Features
        (6, 7.5, 3, 1, 'Admin Features', '#F44336', [
            'Django Admin', 'pgAdmin', 'User Management'
        ]),
        # Technical Features
        (10, 7.5, 3, 1, 'Technical Features', '#795548', [
            'Async Tasks', 'Caching', 'Security Headers'
        ]),
        # Design & UX
        (2, 5, 3, 1, 'Design & UX', '#607D8B', [
            'Responsive Design', 'Animations', 'Glass Morphism'
        ]),
        # Performance
        (6, 5, 3, 1, 'Performance', '#FF5722', [
            'Redis Caching', 'Static File Optimization', 'Gzip Compression'
        ]),
        # Monitoring
        (10, 5, 3, 1, 'Monitoring', '#3F51B5', [
            'Health Checks', 'Logging', 'Error Tracking'
        ]),
    ]
    
    for x, y, w, h, title, color, features in sections:
        # Main section box
        main_box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                                 facecolor=color, edgecolor='black', linewidth=2)
        ax.add_patch(main_box)
        ax.text(x + w/2, y + h/2, title, ha='center', va='center', 
                fontweight='bold', color='white', fontsize=12)
        
        # Feature list below
        for i, feature in enumerate(features):
            feature_y = y - 0.5 - (i * 0.4)
            feature_box = FancyBboxPatch((x + 0.1, feature_y), w - 0.2, 0.3, 
                                        boxstyle="round,pad=0.05",
                                        facecolor='white', edgecolor=color, linewidth=1)
            ax.add_patch(feature_box)
            ax.text(x + w/2, feature_y + 0.15, feature, ha='center', va='center', 
                    fontsize=9, color=color, fontweight='bold')
    
    # Technology stack at bottom
    ax.text(8, 1.5, 'Technology Stack', fontsize=16, fontweight='bold', ha='center')
    
    tech_stack = [
        'Django', 'PostgreSQL', 'Redis', 'Celery', 'Nginx', 
        'Docker', 'Bootstrap', 'JavaScript', 'HTML5', 'CSS3'
    ]
    
    for i, tech in enumerate(tech_stack):
        x_pos = 1 + (i * 1.4)
        tech_box = FancyBboxPatch((x_pos, 0.5), 1.2, 0.5, boxstyle="round,pad=0.05",
                                 facecolor='#E8F5E8', edgecolor='#4CAF50', linewidth=1)
        ax.add_patch(tech_box)
        ax.text(x_pos + 0.6, 0.75, tech, ha='center', va='center', 
                fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('diagrams/feature_map.png', dpi=300, bbox_inches='tight')
    plt.close()

def main():
    """Generate all diagrams"""
    print("🎨 Generating Website Architecture Diagrams...")
    
    # Install requirements
    install_requirements()
    
    # Create diagrams directory
    os.makedirs('diagrams', exist_ok=True)
    
    # Generate all diagrams
    diagrams = [
        ('System Architecture', create_architecture_diagram),
        ('User Flow', create_user_flow_diagram),
        ('Data Flow', create_data_flow_diagram),
        ('Deployment Architecture', create_deployment_diagram),
        ('Feature Map', create_feature_map),
    ]
    
    for name, func in diagrams:
        print(f"Creating {name} diagram...")
        func()
        print(f"✅ {name} diagram created")
    
    print(f"\n📊 All diagrams generated in 'diagrams/' folder:")
    print(f"   - architecture_diagram.png")
    print(f"   - user_flow_diagram.png")
    print(f"   - data_flow_diagram.png")
    print(f"   - deployment_diagram.png")
    print(f"   - feature_map.png")

if __name__ == "__main__":
    main()
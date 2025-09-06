from flask import Blueprint, render_template, request, flash, redirect, url_for
import os

public_bp = Blueprint('public', __name__)

@public_bp.route('/')
def index():
    """Homepage with art slideshow and social links"""
    # Get art files for slideshow
    art_dir = os.path.join('static', 'img', 'art')
    art_files = []
    if os.path.exists(art_dir):
        art_files = [f for f in os.listdir(art_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
        art_files.sort()
    
    return render_template('pages/index.html', art_files=art_files)

@public_bp.route('/store')
def store():
    """Store page with links to Amazon, Etsy, donations"""
    return render_template('pages/store.html')

@public_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page with form"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # TODO: Implement contact form processing
        # For now, just flash a success message
        flash('Thank you for your message! We will get back to you soon.', 'success')
        return redirect(url_for('public.contact'))
    
    return render_template('pages/contact.html')

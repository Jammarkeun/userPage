from flask import Flask, render_template, request, redirect, url_for, flash
import os
import mysql.connector

app = Flask(__name__)

# Configure MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",  # Replace with your MySQL username
    password='',  # Replace with your MySQL password
    database="ecomDB"  # Replace with your database name
)

# Configure upload folder and allowed extensions
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    cursor = db.cursor(dictionary=True)
    user_id = 1  # Example: Replace with session-based user ID in real implementation

    if request.method == 'POST':
        # Handle profile updates
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        cursor.execute(
            "UPDATE users SET name = %s, email = %s, phone = %s WHERE id = %s",
            (name, email, phone, user_id)
        )
        db.commit()

        # Handle profile picture upload
        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            if file and allowed_file(file.filename):
                filename = f"user_{user_id}_" + file.filename
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                # Update profile picture in database
                cursor.execute(
                    "UPDATE users SET profile_picture = %s WHERE id = %s",
                    (filename, user_id)
                )
                db.commit()
                flash("Profile updated successfully!", "success")
            else:
                flash("Invalid file format. Only PNG, JPG, JPEG, and GIF are allowed.", "danger")

        return redirect(url_for('profile'))

    # Fetch user details
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    return render_template('profile.html', user=user)

@app.route('/order-history')
def order_history():
    return render_template('order_history.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/security')
def security():
    return render_template('resetPassword.html')

@app.route('/logout')
def logout():
    # Logic for logout (e.g., clearing session)
    return "Logged out successfully."

if __name__ == '__main__':
    app.run(debug=True)

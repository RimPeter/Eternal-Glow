# Eternal Glow

![Eternal Glow Logo](static/images/MAINLOGO_2.png)

*A private sector dermatology clinic.*
## Description

**Eternal Glow** is a private sector dermatology clinic specializing in skincare services. Our mission is to provide top-notch dermatological care accessible to a broader audience through our online platform.

### Brief Overview

Clients can:

- **Register** for a personalized account.
- **Book** appointments for a variety of skincare services.
- **Manage** their bookings and account details with full CRUD (Create, Read, Update, Delete) functionalities.

### Motivation

The motivation behind Eternal Glow's website is to extend our reach and make our services accessible to clients outside our immediate area. We aim to provide a seamless online experience for booking and managing skincare appointments.

### Problem It Solves

By offering an online platform, Eternal Glow overcomes geographical limitations, allowing the clinic to connect with clients who might not have discovered our services otherwise. This enhances convenience for clients and expands our business footprint.

## Installation

### Prerequisites

Before installing **Eternal Glow**, ensure you have the following software and tools installed:

- **Python 3.7+**
- **pip** (Python package manager)
- **virtualenv** (optional but recommended)

The project requires the following Python packages:

```plaintext
asgiref==3.8.1
certifi==2024.8.30
cffi==1.17.1
charset-normalizer==3.3.2
crispy-bootstrap5==2024.2
cryptography==43.0.1
dj-database-url==2.2.0
Django==5.1
django-allauth==64.2.0
django-crispy-forms==2.3
gunicorn==23.0.0
idna==3.8
oauthlib==3.2.2
packaging==24.1
pillow==10.4.0
psycopg2-binary==2.9.9
pycparser==2.22
PyJWT==2.9.0
python-decouple==3.8
requests==2.32.3
requests-oauthlib==2.0.0
sqlparse==0.5.1
stripe==10.11.0
typing_extensions==4.12.2
tzdata==2024.1
urllib3==2.2.2
whitenoise==6.7.0
```
### Installation Steps

Follow these steps to set up **Eternal Glow** on your local machine:

**Clone the Repository**

   Clone the project from the repository to your local machine:

   ```bash
   git clone https://github.com/RimPeter/Eternal-Glow.git
   cd eternal-glow
```
Create a Virtual Environment (optional but recommended)

Create and activate a virtual environment to manage dependencies:

On macOS and Linux:

```bash
Copy code
python3 -m venv venv
source venv/bin/activate
```
On Windows:

```bash
Copy code
python -m venv venv
venv\Scripts\activate
```
Install Dependencies

Install all required Python packages using pip:

```bash
Copy code
pip install -r requirements.txt
```
Set Up Environment Variables

Create a .env file in the project root directory to store environment variables:

```bash
Copy code
touch .env
```
Add the necessary configurations to the .env file:

```dotenv
Copy code
DEBUG=True
SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///db.sqlite3
```
Note: Replace your_secret_key_here with a securely generated secret key.

Apply Database Migrations

Apply migrations to set up the database schema:

```bash
Copy code
python manage.py migrate
```
Create a Superuser (optional)

If you want to access the Django admin panel, create a superuser account:

```bash
Copy code
python manage.py createsuperuser
```
Collect Static Files

Collect all static files into a single directory:

```bash
Copy code
python manage.py collectstatic
```
Note: When prompted, type yes to confirm.

Run the Development Server

Start the Django development server:

```bash
Copy code
python manage.py runserver
```
Access the Application

Open your web browser and navigate to:

```url
Copy code
http://127.0.0.1:8000/
```

Deployment
Deploying Eternal Glow to a production environment involves several steps to ensure the application runs smoothly, securely, and efficiently. Below is a comprehensive guide to deploying the application, including setting up the database and configuring the server.

Preparing for Deployment
Choose a Hosting Provider

Select a reliable hosting provider that supports Django applications. Popular choices include:

Heroku
AWS (Amazon Web Services)
DigitalOcean
PythonAnywhere
Azure
Set Up a Production Environment

Create a Virtual Environment:

```bash
Copy code
python3 -m venv venv
source venv/bin/activate
```
Install Dependencies:

```bash
Copy code
pip install -r requirements.txt
```
Set DEBUG to False:

In your .env file, ensure that:

```dotenv
Copy code
DEBUG=False
```
Configure Allowed Hosts:

Add your domain or server IP to the ALLOWED_HOSTS in settings.py:

```python
Copy code
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
```
Setting Up the Database
For production, it's recommended to use a more robust database system like PostgreSQL instead of SQLite.

Install PostgreSQL

On Ubuntu:

```bash
Copy code
sudo apt update
sudo apt install postgresql postgresql-contrib
```
On macOS (using Homebrew):

```bash
Copy code
brew install postgresql
brew services start postgresql
```
Create a Database and User

```bash
Copy code
sudo -u postgres psql
```
Inside the PostgreSQL shell:

```sql
Copy code
CREATE DATABASE eternal_glow_db;
CREATE USER eternal_user WITH PASSWORD 'securepassword';
ALTER ROLE eternal_user SET client_encoding TO 'utf8';
ALTER ROLE eternal_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE eternal_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE eternal_glow_db TO eternal_user;
\q
```
Configure DATABASE_URL

Update the .env file with the PostgreSQL database URL:

```dotenv
Copy code
DATABASE_URL=postgres://eternal_user:securepassword@localhost:5432/eternal_glow_db
```
Apply Migrations

```bash
Copy code
python manage.py migrate
```
Configuring the Server
Install and Configure Gunicorn

Gunicorn is a Python WSGI HTTP Server for UNIX. Install it using pip:

```bash
Copy code
pip install gunicorn
```
Test Gunicorn by running:

```bash
Copy code
gunicorn eternal_glow.wsgi
```
Set Up a Reverse Proxy with Nginx

Deploying the Application
Collect Static Files

```bash
Copy code
python manage.py collectstatic
```
Restart Services

```bash
Copy code
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```
Secure the Application with SSL

It's crucial to secure your application with SSL. You can obtain a free SSL certificate from Let's Encrypt:

```bash
Copy code
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```
Follow the prompts to complete the SSL setup.


Activate the Virtual Environment

```bash
Copy code
source venv/bin/activate
```



jobs:
  build:
```
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:12
        env:
          POSTGRES_USER: eternal_user
          POSTGRES_PASSWORD: securepassword
          POSTGRES_DB: eternal_glow_db
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run migrations
      run: |
        python manage.py migrate
    - name: Run tests
      run: |
        python manage.py test
```
Commit and Push:

```bash
Copy code
git add .
git commit -m "Add workflow"
git push origin main
```

## Usage

### Basic Usage

**Eternal Glow** provides a user-friendly interface for clients to manage their skincare needs effortlessly. Here’s how you can navigate and utilize the platform:

1. **Register an Account**
   - Navigate to the **Register** page.
   - Fill in the required details to create a new account.
   
2. **Login**
   - Go to the **Login** page.
   - Enter your credentials to access your personalized dashboard.
   
3. **Browse Services**
   - Explore the range of skincare treatments and services offered.
   
4. **Create a Booking**
   - Select your desired service and choose a convenient time slot.
   - Confirm your booking details to secure your appointment.
   
5. **Manage Bookings**
   - View your upcoming appointments in the **Booking List**.
   - Update or cancel your bookings as needed through the **Manage Booking** section.

### Screenshots/Demos

Visual representations can help you better understand the workflow and features of **Eternal Glow**. Below are screenshots showcasing various parts of the application:

- **Home Page**

  ![Home Page](static/images/readme/home.png)

  *The welcoming home page provides an overview of our services and easy navigation options.*

- **Services Page**

  ![Services](static/images/readme/treatments.png)

  *Browse through our comprehensive list of skincare treatments tailored to your needs.*

- **Registration Page**

  ![Register Page](static/images/readme/register-page.png)

  *Create a new account by providing your personal information.*

- **Login Page**

  ![Login Page](static/images/readme/login-page.png)

  *Access your account securely using your registered credentials.*

- **Create Booking**

  ![Create Booking](static/images/readme/create-booking.png)

  *Select a service and schedule your appointment with ease.*

- **Booking List**

  ![Booking List](static/images/readme/booking-list.png)

  *View all your upcoming and past bookings in one place.*

- **Manage Booking**

  ![Manage Booking](static/images/readme/manage-booking.png)

  *Update or cancel your appointments directly from the management interface.*

## Facebook Business Page

Connect with **Eternal Glow** on our official [Facebook Business Page](https://www.facebook.com/eternalglowclinic) to stay updated with the latest news, skincare tips, and exclusive offers.

![Eternal Glow on Facebook](static/images/readme/facebook.png)

### Why Follow Us on Facebook?

- **Stay Informed**: Receive real-time updates about our services, promotions, and events.
- **Expert Insights**: Access valuable skincare advice and tips from our experienced dermatologists.
- **Community Engagement**: Join a community of like-minded individuals who are passionate about skincare and wellness.
- **Exclusive Content**: Enjoy special content, including tutorials, behind-the-scenes looks, and client testimonials.
- **Interactive Support**: Get your questions answered and receive personalized recommendations directly through our Facebook page.

### How to Connect

1. **Visit Our Page**: Click on the [Eternal Glow Facebook Page](https://www.facebook.com/eternalglowclinic) link.
2. **Like and Follow**: Click the "Like" and "Follow" buttons to start receiving updates.
3. **Engage with Us**: Like, comment, and share our posts to engage with our community and stay involved.

By following our Facebook Business Page, you'll be the first to know about new services, special discounts, and important announcements. Join our online community today and take a step towards achieving radiant and healthy skin with **Eternal Glow**!

---


## Resources

### Tools and Technologies

- **[Django](https://www.djangoproject.com/)**: The primary web framework used to build the backend of **Eternal Glow**, providing a robust and scalable foundation for our application.

- **[Google](https://www.google.com/)**: Utilized extensively for research, troubleshooting, and accessing a wealth of tutorials and documentation that facilitated efficient problem-solving throughout the development process.

- **[GPT-4 by OpenAI](https://openai.com/product/gpt-4)**: Assisted in generating code snippets, improving documentation, and enhancing the overall quality of written content within the project.

### Design and Aesthetics

- **[Image Color Picker](https://imagecolorpicker.com/)**: Employed to select and harmonize the color palette, ensuring that the website's design is both visually appealing and consistent with our brand identity.

- **[Pure Skin Clinic Hessle](https://pureskinclinic.uk/pure-skin-clinic-hessle/)**: Served as a reference for layout and design inspiration, helping us craft a user-friendly and aesthetically pleasing interface tailored to our target audience.

### Learning and Development

- **[YouTube](https://www.youtube.com/)**: A valuable resource for tutorials, walkthroughs, and best practices in Django development, front-end design, and deployment strategies that enhanced our team's skill set and project execution.

### Additional Resources

- **[Bootstrap](https://getbootstrap.com/)**: Integrated for responsive design, ensuring that **Eternal Glow** is accessible and functions flawlessly across various devices and screen sizes.

- **[Font Awesome](https://fontawesome.com/)**: Utilized for adding scalable vector icons that enhance the user interface and improve navigation.

## Manual Testing
In lack of automated tests, thorough manual testing has been conducted to ensure that all views function correctly and provide a seamless user experience. The following Django views have been tested to verify their functionality, usability, and reliability:

Authentication and User Management

### register_admin

Purpose: Handles the registration of new admin users.

Testing: Verified that admin accounts are created securely, with proper validation and access permissions.

### register_patient

Purpose: Manages patient registration and profile creation.

Testing: Ensured that patients can register successfully, with all required fields validated and profiles correctly associated with user accounts.

### login

Purpose: Facilitates user authentication.

Testing: Confirmed that users can log in with valid credentials and receive appropriate error messages for invalid attempts.

### logout

Purpose: Handles user logout functionality.

Testing: Verified that users can securely log out, terminating their sessions without errors.

### change_password

Purpose: Allows users to update their passwords.

Testing: Ensured that password changes are processed correctly, with validations for old and new passwords.

### delete_user

Purpose: Enables the deletion of user accounts.

Testing: Confirmed that user accounts are deleted securely, with appropriate confirmations and error handling.

### create_patient_profile

Purpose: Facilitates the creation of detailed patient profiles.

Testing: Verified that patient profiles are created with all necessary information and correctly linked to user accounts.
Booking and Appointment Management

### create_booking

Purpose: Allows patients to create new bookings for skincare services.

Testing: Tested booking creation with various inputs, ensuring duplicate bookings are prevented and bookings are correctly linked to patients.

### booking_failed

Purpose: Displays an error message when a booking attempt fails.

Testing: Verified that appropriate error messages are shown for duplicate bookings and other failure scenarios.

### booking_list

Purpose: Displays a list of all bookings associated with a patient.

Testing: Ensured that bookings are correctly listed, sorted, and accessible only to the respective patient.

### manage_booking

Purpose: Provides functionalities to manage existing bookings, including updates and cancellations.

Testing: Tested updating booking details, changing dates and products, and canceling bookings with and without payments.

### change_booking_date

Purpose: Allows patients to change the date and time of their bookings.

Testing: Verified date validations, conflict checks, and successful updates of booking dates and time slots.

### change_booking_product

Purpose: Enables patients to change the service/product associated with their bookings.

Testing: Tested product changes with scenarios involving price differences, additional payments, and refunds.

### cancel_booking

Purpose: Facilitates the cancellation of bookings.

Testing: Ensured that cancellations process refunds when applicable and delete bookings securely.

### payment_cancel

Purpose: Handles scenarios where a payment is canceled.

Testing: Verified that users are appropriately notified and that the application state reflects the canceled payment.
Payment Processing

### create_checkout_session

Purpose: Initiates the Stripe checkout session for payments.

Testing: Confirmed that checkout sessions are created with correct payment details and that users are redirected appropriately.

### payment_success

Purpose: Processes successful payment confirmations.

Testing: Ensured that payment statuses are updated correctly and that users receive confirmation messages.

### stripe_webhook

Purpose: Handles incoming Stripe webhook events.

Testing: Verified that webhook events are processed accurately, updating booking statuses based on payment outcomes.

### handle_payment_intent_succeeded

Purpose: Updates bookings upon successful payment intents.

Testing: Confirmed that bookings are marked as paid and associated with the correct payment intents.

### handle_payment_intent_failed

Purpose: Manages failed payment intents.

Testing: Ensured that failed payments are handled gracefully, notifying users and maintaining data integrity.

### product_change_success

Purpose: Finalizes product changes after additional payments.

Testing: Verified that product updates are processed correctly upon successful additional payments.

## Business Model and Marketing Strategies

### E-commerce Business Model

**Eternal Glow** operates on a robust e-commerce business model designed to provide exceptional dermatological services and high-quality skincare products to our clients. Our model is built around the following key components:

#### 1. **Revenue Streams**

- **Service Bookings:**
  - **Online Appointments:** Clients can conveniently book a variety of dermatological services through our user-friendly online platform.
  - **Subscription Plans:** Offer subscription-based services for regular skincare treatments, providing clients with consistent care and generating recurring revenue.

- **Product Sales:**
  - **Skincare Products:** Sell a curated selection of premium skincare products, including creams, serums, and treatments recommended by our dermatologists.
  - **Bundles and Kits:** Provide bundled products and treatment kits tailored to specific skin concerns, encouraging higher average order values.

- **Consultation Fees:**
  - **Virtual Consultations:** Offer virtual dermatology consultations for clients seeking expert advice without visiting the clinic in person.
  - **Personalized Treatment Plans:** Develop customized skincare plans for clients, adding value through personalized care.

#### 2. **Target Market**

- **Demographics:**
  - **Age:** Primarily targeting adults aged 25-55 who are proactive about skincare and interested in maintaining healthy, radiant skin.
  - **Gender:** Services and products cater to all genders, with specialized treatments for diverse skin types and concerns.

- **Psychographics:**
  - **Health-Conscious Individuals:** Clients who prioritize their health and wellness, seeking professional dermatological care.
  - **Beauty Enthusiasts:** Individuals passionate about beauty and skincare, looking for effective products and treatments.

#### 3. **Value Proposition**

- **Expertise and Trust:** Leveraging the expertise of certified dermatologists to offer reliable and effective skincare solutions.
- **Convenience:** Providing a seamless online booking system and e-commerce platform for easy access to services and products.
- **Personalization:** Offering tailored treatment plans and product recommendations to meet individual skincare needs.
- **Quality Assurance:** Ensuring all products sold are of the highest quality and recommended by our dermatology experts.

### Marketing Strategies

To effectively reach and engage our target audience, **Eternal Glow** employs a multifaceted marketing strategy that combines digital marketing, content creation, and community engagement. Our strategies include:

#### 1. **Digital Marketing**

- **Search Engine Optimization (SEO):**
  - Optimize website content with relevant keywords to improve search engine rankings and drive organic traffic.
  - Implement on-page SEO techniques, including meta tags, alt texts for images, and high-quality backlinks.

- **Pay-Per-Click (PPC) Advertising:**
  - Utilize platforms like Google Ads and Bing Ads to run targeted advertising campaigns, attracting potential clients actively searching for skincare services and products.
  - Monitor and adjust campaigns based on performance metrics to maximize ROI.

- **Social Media Marketing:**
  - Maintain active profiles on platforms such as Facebook, Instagram, and Twitter to engage with the community, share updates, and promote services and products.
  - Use targeted ads and sponsored posts to reach a broader and more specific audience.

#### 2. **Content Marketing**

- **Blogging:**
  - Publish informative and engaging blog posts on skincare tips, treatment options, and the latest dermatology trends to establish authority and provide value to visitors.
  - Incorporate SEO best practices to enhance visibility and attract organic traffic.

- **Video Content:**
  - Create tutorial videos, behind-the-scenes looks, and client testimonials to showcase expertise and build trust with potential clients.
  - Share videos on YouTube and social media channels to increase reach and engagement.

- **Email Marketing:**
  - Develop a comprehensive email marketing strategy to nurture leads, inform clients about new services and products, and promote special offers.
  - Segment email lists to deliver personalized content based on client interests and behaviors.

#### 3. **Influencer Partnerships**

- **Collaborations with Beauty Influencers:**
  - Partner with skincare and beauty influencers to promote **Eternal Glow** services and products, leveraging their reach and credibility.
  - Offer exclusive discounts and affiliate programs to incentivize influencer promotions.

- **Guest Blogging and Features:**
  - Contribute guest posts to reputable beauty and health websites, enhancing brand visibility and driving referral traffic.

#### 4. **Local Marketing and Community Engagement**

- **Local SEO:**
  - Optimize for local search queries to attract clients within the clinic’s geographical area.
  - Ensure consistent business listings across online directories like Google My Business, Yelp, and Bing Places.

- **Events and Workshops:**
  - Host virtual and in-person events, such as skincare workshops and Q&A sessions with dermatologists, to engage the community and showcase expertise.
  - Participate in local health and wellness fairs to increase brand presence and connect with potential clients.

#### 5. **Customer Loyalty Programs**

- **Rewards and Referrals:**
  - Implement a rewards program that offers points for bookings and purchases, redeemable for discounts or exclusive products.
  - Encourage satisfied clients to refer friends and family by offering incentives for successful referrals.

- **Personalized Offers:**
  - Use data analytics to understand client preferences and behaviors, enabling the delivery of personalized offers and recommendations that enhance customer satisfaction and loyalty.

#### 6. **Public Relations (PR)**

- **Press Releases:**
  - Distribute press releases to announce new services, product launches, and significant milestones, garnering media coverage and enhancing credibility.
  
- **Media Outreach:**
  - Engage with local and national media outlets to feature **Eternal Glow** in health and beauty segments, increasing brand recognition.

### Measuring Success

To ensure the effectiveness of our marketing strategies, **Eternal Glow** employs various metrics and analytics tools:

- **Website Analytics:**
  - Use Google Analytics to monitor website traffic, user behavior, and conversion rates, identifying areas for improvement and optimizing user experience.

- **Social Media Insights:**
  - Track engagement rates, follower growth, and campaign performance on social media platforms to assess the impact of our social media efforts.

- **Email Campaign Metrics:**
  - Analyze open rates, click-through rates, and conversion rates for email campaigns to refine content and targeting strategies.

- **Customer Feedback:**
  - Collect and review client feedback through surveys and reviews to understand satisfaction levels and identify opportunities for enhancement.

By integrating these comprehensive marketing strategies with our e-commerce business model, **Eternal Glow** aims to establish a strong online presence, attract and retain a loyal client base, and drive sustainable growth in the competitive dermatology market.

---


## Brief Descriptions of Key Missing Features
### Password Reset Functionality: 
Allow users to securely reset their passwords if forgotten.

### Email Verification Upon Registration: 
Ensure users verify their email addresses to activate accounts.

### Two-Factor Authentication (2FA): 
Provide an additional security layer during user login.

### Accessibility Features: 
Make the application usable for individuals with disabilities by adhering to accessibility standards.

### Multi-Language Support: 
Enable the application to support multiple languages for a diverse user base.

### Regular Data Backups: 
Implement automated backups to prevent data loss.

### Real-Time Performance Monitoring: 
Continuously monitor system performance to identify and address issues promptly.

### Interactive Booking Calendar: 
Offer a visual calendar interface for users to select booking dates and view availability.

### Personalized User Dashboard: 
Create a dashboard that provides users with quick access to their bookings, profile, and notifications.

### Export Booking History: 
Allow users to export their booking data for personal records.


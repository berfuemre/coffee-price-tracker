**Description**

Product Tracker is a web application designed to help users track products from various online retailers. Users can submit product URLs, and the application will scrape the product information and offers, saving them in a database. This allows users to monitor price changes and availability over time, making it easier to make informed purchasing decisions.

**Features**

1-  URL Tracking: Users can submit product URLs to be tracked for updates on prices and availability.

2-  Product Scraping: The application extracts product information such as name, description, SKU, brand, and offers from the provided URLs.

3- Database Integration: All product data, offers, and tracked URLs are stored in a SQLite database, allowing for persistent storage and retrieval of information.

4- User Notifications: Integration with Twilio for sending SMS notifications when price drops or products become available.

5- Logging: Detailed logging for monitoring application activity and troubleshooting potential issues.



**Technologies Used**


**Flask:** A lightweight web framework for building the application.

**SQLAlchemy:** An ORM (Object-Relational Mapping) library for managing database interactions.

**SQLite**: A lightweight database for storing product and user data.

**httpx:** An HTTP client for making requests to the product URLs.

**Twilio:** A cloud communications platform for sending SMS notifications.

**Python:** The programming language used for building the application.


**Skills Demonstrated**

**Web Development:** Building and deploying a web application using Flask.

**Database Management:** Designing and implementing a database schema using SQLAlchemy.

**API Integration:** Utilizing Twilio for SMS notifications and httpx for making HTTP requests.

**Data Scraping:** Extracting and processing product information from various websites.

**Logging and Debugging:** Implementing logging to monitor application performance and troubleshoot issues.

**Version Control:** Using Git for version control and collaboration.



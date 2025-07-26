# 🤖 Kerala Services Bot

> **Your AI-powered assistant for Kerala Government Services**

A comprehensive chatbot that helps citizens access information about Kerala government services, register complaints, and get real-time assistance. Built with modern web technologies and AI integration.

![Kerala Services Bot](https://img.shields.io/badge/Status-Live-brightgreen)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![React](https://img.shields.io/badge/React-18.0+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)
![MongoDB](https://img.shields.io/badge/MongoDB-5.0+-green)

## ✨ Features

### 🗣️ **Intelligent Chat Interface**
- **AI-Powered Responses**: Powered by Google's Gemini AI for accurate and helpful responses
- **Natural Language Processing**: Understands queries in natural language
- **Real-time Streaming**: Instant responses with typing indicators
- **Markdown Support**: Rich text formatting for better readability

### 🏛️ **Government Services Coverage**
- **Birth & Death Certificates**: Application process, fees, and requirements
- **Voter ID Services**: Registration, corrections, and updates
- **Driving Licenses**: New applications, renewals, and modifications
- **Property Tax**: Online payment and certificate downloads
- **Utility Bills**: Electricity, water, and telephone bill payments
- **Ration Cards**: Applications, member management, and status tracking
- **And much more...**

### 📝 **Complaint Management System**
- **Easy Registration**: Simple form to register complaints
- **Email Notifications**: Automatic email alerts to relevant departments
- **Complaint Tracking**: Track status using complaint ID or contact number
- **Department Mapping**: Smart routing to appropriate government departments

### 🎨 **Modern User Interface**
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Dark/Light Mode**: Toggle between themes for comfortable viewing
- **PDF Export**: Download chat responses as PDF documents
- **Accessibility**: User-friendly interface with clear navigation

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 16+
- MongoDB (local or cloud)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/kerala-services-bot.git
   cd kerala-services-bot
   ```

2. **Backend Setup**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Set environment variables
   export MONGO_URI="your_mongodb_connection_string"
   export SENDER_EMAIL="your_gmail@gmail.com"
   export SENDER_PASSWORD="your_gmail_app_password"
   
   # Run backend
   cd backend
   uvicorn main:app --reload
   ```

3. **Frontend Setup**
   ```bash
   cd frontend/frontend2
   npm install
   npm start
   ```

4. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **MongoDB**: NoSQL database for storing complaints and data
- **Google Gemini AI**: Advanced AI model for intelligent responses
- **SMTP**: Email functionality for complaint notifications
- **RapidFuzz**: Fuzzy string matching for service identification

### Frontend
- **React 18**: Modern JavaScript library for building user interfaces
- **Axios**: HTTP client for API communication
- **React Markdown**: Markdown rendering for rich text
- **jsPDF**: PDF generation for chat exports
- **React Icons**: Beautiful icon library

### Infrastructure
- **Git**: Version control
- **GitHub**: Code repository
- **Render**: Backend hosting
- **Vercel**: Frontend hosting
- **MongoDB Atlas**: Cloud database

## 📋 API Endpoints

### Chat & Services
- `POST /ask` - Get AI-powered responses about government services
- `GET /` - Health check endpoint

### Complaint Management
- `POST /register_complaint` - Register a new complaint
- `POST /track_complaint` - Track complaint status

## 🎯 Usage Examples

### Asking About Services
```
User: "How to apply for birth certificate?"
Bot: Provides detailed information about the application process, 
     required documents, fees, and processing time.
```

### Registering Complaints
```
User: Clicks "Register Complaint" button
Form: Pre-fills with service name and allows user to add details
Email: Automatically sent to relevant department with complaint details
```

### Tracking Complaints
```
User: Enters complaint ID or contact number
System: Returns complaint status and details
```

## 🔧 Configuration

### Environment Variables
```bash
MONGO_URI=mongodb://localhost:27017/
SENDER_EMAIL=your_gmail@gmail.com
SENDER_PASSWORD=your_gmail_app_password
GEMINI_API_KEY=your_gemini_api_key
```

### Department Email Mapping
```python
department_emails = {
    "voter id": "voter_dept@kerala.gov.in",
    "birth certificate": "civil_registration@kerala.gov.in",
    # Add more departments as needed
}
```

## 📊 Features in Detail

### 🤖 AI Integration
- **Context-Aware Responses**: Understands service-specific queries
- **Multi-language Support**: Handles various question formats
- **Service Matching**: Fuzzy matching for accurate service identification
- **Real-time Processing**: Instant responses with streaming

### 📧 Email System
- **Automatic Routing**: Sends complaints to appropriate departments
- **Reply-To Headers**: Enables direct communication between users and departments
- **Error Handling**: Graceful failure handling with logging
- **Template System**: Professional email formatting

### 🗄️ Data Management
- **MongoDB Integration**: Scalable NoSQL database
- **Complaint Tracking**: Unique IDs for easy reference
- **Data Validation**: Input sanitization and validation
- **Backup & Recovery**: Robust data management

## 🌟 Key Benefits

### For Citizens
- **24/7 Availability**: Access services anytime, anywhere
- **Instant Information**: Quick answers to common questions
- **Easy Complaint Filing**: Simple, user-friendly process
- **Transparency**: Track complaint status in real-time

### For Government Departments
- **Automated Processing**: Reduces manual workload
- **Email Notifications**: Immediate complaint alerts
- **Data Analytics**: Insights into common issues
- **Improved Efficiency**: Faster response times

## 🔒 Security Features

- **Input Validation**: Sanitizes all user inputs
- **Rate Limiting**: Prevents abuse and spam
- **Error Handling**: Graceful error management
- **Secure Email**: SMTP with authentication
- **CORS Protection**: Cross-origin request handling

## 🚀 Deployment

### Backend (Render)
1. Connect GitHub repository to Render
2. Set environment variables
3. Deploy with build command: `pip install -r requirements.txt`
4. Start command: `uvicorn backend.main:app --host 0.0.0.0 --port 10000`

### Frontend (Vercel)
1. Import repository to Vercel
2. Set environment variables for API URL
3. Deploy automatically on push

### Database (MongoDB Atlas)
1. Create free cluster
2. Set up database user
3. Configure IP access
4. Update connection string

## 🤝 Contributing

We welcome contributions! Please feel free to submit a Pull Request.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

- **Issues**: Report bugs and feature requests on GitHub
- **Documentation**: Check the code comments for detailed explanations
- **Community**: Join our discussions for help and ideas

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Kerala Government**: For providing comprehensive service information
- **Google Gemini**: For powerful AI capabilities
- **Open Source Community**: For the amazing tools and libraries
- **Contributors**: Everyone who helps improve this project

---

**Made with ❤️ for the people of Kerala**

<<<<<<< HEAD
*Empowering citizens with easy access to government services through technology.* 
=======
*Empowering citizens with easy access to government services through technology.*
>>>>>>> 34117e7fd9979c5e99e4923ad3e3c7734c5b7b30

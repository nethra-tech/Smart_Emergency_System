# 🚑 Smart Emergency Response System

A comprehensive emergency response system integrated with India's 112 emergency service.

## 🛠️ Technology Stack

### Frontend
| Technology | Purpose |
|------------|---------|
| **HTML5** | Structure of web pages |
| **CSS3** | Responsive UI design with ambulance theme |
| **JavaScript (ES6)** | Emergency logic, form handling, location access |
| **Leaflet.js** | Maps and route visualization |

## 📁 Project Structure

```
Smart-Emergency-Response-System/
├── index.html          # Main landing page
├── emergency.html      # Emergency form & processing
├── login.html          # Phone & OTP login
├── dashboard.html      # User dashboard
├── track.html          # Location tracking
├── about.html          # About us page
├── learn.html         # Emergency skills tutorials
├── profile.html       # User profile
├── chat.html          # Chat support
└── app.css            # All styling (ambulance theme)
```

## 🚀 Running the Project

Simply open `index.html` in your web browser - no server needed!

All features work locally using JavaScript:
- Auto location detection
- Hospital selection formula
- OTP verification (demo)
- Emergency number dialing
- Live maps

## 🏥 Hospital Selection Formula

```
Score = Distance + Bed Availability + ICU Availability + Emergency Type Match + Severity
```

## 📱 Features

### Emergency Flow
1. Select emergency type and people count
2. Auto-detect location via GPS
3. Calculate best hospital using formula
4. Show ambulance ETA and route

### Login Flow
1. Enter phone number
2. Receive and verify OTP (Demo OTP: 123456)
3. Access dashboard

### Dashboard Services
- Emergency Contacts (100, 101, 102, 112, etc.)
- Track Me - Live location sharing
- About Us - Mission and values
- Chat Support
- SOS Without Signal (SMS fallback)
- Learn Emergency Skills (CPR, First Aid, etc.)
- User Profile
- Family Contacts

## 🎨 Theme
- **Primary Color:** Blue (#1e88e5)
- **Emergency Color:** Red (#e53935)
- **Background:** Dark blue gradient
- **112 India Integration** on all pages

## 📞 Emergency Numbers
| Service | Number |
|---------|--------|
| Police | 100 |
| Fire | 101 |
| Ambulance | 102 |
| Women Helpline | 1091 |
| Child Helpline | 1098 |
| Universal Emergency | 112 |

---
Built with ❤️ for emergency response

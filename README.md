# Library Management System

A modern, comprehensive library management system designed for administrators to efficiently manage books, authors, and library operations.

## 🚀 Introduction

Library System is a professional library management solution that provides administrators with powerful tools to manage their library's inventory, author database, and operational workflows. Built with modern web technologies, it offers an intuitive interface for seamless library administration.

## ✨ Features

### 📚 Book Management
- Add, edit, and delete book records
- Comprehensive book information tracking (ISBN, title, author, publication year)
- Advanced search and filtering capabilities
- Data validation and duplicate prevention
- Bulk operations and batch processing

### 👥 Author Management
- Complete author database management
- Author-book relationship tracking
- Advanced search functionality
- Visual display of author portfolios

### 🔍 Advanced Search & Analytics
- Multi-field search across all database fields
- Real-time filtering and sorting
- Table pagination for large datasets
- Comprehensive data visualization

### 💻 User Experience
- Responsive design for desktop and mobile devices
- Modern, intuitive admin interface
- Real-time data updates
- Professional modal-based editing
- Toast notifications for user feedback

### 🔒 Administration Features
- Secure admin authentication
- Data validation and integrity checks
- Comprehensive error handling
- Activity logging and audit trails

## 🛠️ Technology Stack

- **Frontend**: React, TypeScript, Tailwind CSS
- **Backend**: Supabase (PostgreSQL, Real-time APIs)
- **UI Components**: Radix UI, Shadcn/ui
- **State Management**: React Query (TanStack Query)
- **Build Tool**: Vite
- **Deployment**: Modern Cloud Platform

## 📦 Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd library-system
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
cp .env.example .env.local
# Configure your Supabase credentials
```

4. Start the development server:
```bash
npm run dev
```

5. Open your browser and navigate to `http://localhost:5173`

## 🚀 Usage

### Getting Started
1. Access the admin dashboard at the application URL
2. Use the navigation bar to switch between Books and Authors management
3. Add new records using the input forms
4. Search and filter data using the search functionality
5. Edit or delete records using the action buttons in each table row

### Managing Books
- **Add Books**: Fill in all required fields (Author name, ISBN, Title, Year) and click "ADD"
- **Search Books**: Use the search bar to find books by any field
- **Edit Books**: Click the pencil icon to open the edit modal
- **Delete Books**: Click the trash icon to remove a book record

### Managing Authors
- **Add Authors**: Enter author's first and last name, then click "ADD"
- **View Author Books**: Click "SHOW" to see all books by each author
- **Search Authors**: Use the search functionality to find specific authors
- **Edit/Delete**: Use the action buttons to modify author records

## 📁 Project Structure

```
library-system/
├── src/
│   ├── components/          # React components
│   ├── pages/              # Application pages
│   ├── lib/                # Utility functions
│   ├── hooks/              # Custom React hooks
│   └── types/              # TypeScript definitions
├── public/                 # Static assets
└── docs/                   # Documentation
```

## 🤝 Contributing

We welcome contributions to Library System! Please feel free to submit issues, feature requests, or pull requests.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Library System** - Streamlining library management for the digital age.

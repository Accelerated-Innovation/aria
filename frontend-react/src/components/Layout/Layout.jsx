// src/components/Layout/Layout.jsx
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import { useState } from 'react';
import { Menu } from 'lucide-react';

const Layout = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  
  return (
    <div className="flex h-screen bg-gray-100">
      {/* Mobile sidebar toggle */}
      <button 
        className="md:hidden fixed z-50 top-4 left-4 p-2 bg-white rounded-md shadow-md"
        onClick={() => setIsSidebarOpen(prev => !prev)}
      >
        <Menu size={24} />
      </button>
      
      {/* Sidebar */}
      <div 
        className={`md:relative fixed inset-y-0 left-0 z-40 w-64 bg-white shadow-lg transition-transform transform 
          ${isSidebarOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'}`}
      >
        <Sidebar onClose={() => setIsSidebarOpen(false)} />
      </div>
      
      {/* Main content */}
      <div className="flex-1 overflow-hidden">
        <Outlet />
      </div>
      
      {/* Backdrop for mobile */}
      {isSidebarOpen && (
        <div 
          className="md:hidden fixed inset-0 z-30 bg-black bg-opacity-50"
          onClick={() => setIsSidebarOpen(false)}
        />
      )}
    </div>
  );
};

export default Layout;
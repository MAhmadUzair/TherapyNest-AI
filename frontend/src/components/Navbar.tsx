import React from 'react';
import { Link } from 'react-router-dom';
import { Brain, Menu, X } from 'lucide-react';

const Navbar = () => {
  const [isOpen, setIsOpen] = React.useState(false);

  return (
    <nav className="bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-2">
              <Brain className="h-8 w-8 text-indigo-600" />
              <span className="font-display text-xl font-bold text-gray-900">TherapyNest AI</span>
            </Link>
          </div>
          
          <div className="hidden sm:flex sm:items-center sm:space-x-8">
            <Link to="/" className="text-gray-700 hover:text-indigo-600 px-3 py-2 font-medium">
              Home
            </Link>
            <Link to="/chat" className="text-gray-700 hover:text-indigo-600 px-3 py-2 font-medium">
              Chat Therapy
            </Link>
            <Link to="/voice" className="text-gray-700 hover:text-indigo-600 px-3 py-2 font-medium">
              Voice Therapy
            </Link>
            <button className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700">
              Get Started
            </button>
          </div>

          <div className="sm:hidden flex items-center">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="text-gray-500 hover:text-gray-700"
            >
              {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      {isOpen && (
        <div className="sm:hidden">
          <div className="pt-2 pb-3 space-y-1">
            <Link
              to="/"
              className="block px-3 py-2 text-base font-medium text-gray-700 hover:text-indigo-600"
            >
              Home
            </Link>
            <Link
              to="/chat"
              className="block px-3 py-2 text-base font-medium text-gray-700 hover:text-indigo-600"
            >
              Chat Therapy
            </Link>
            <Link
              to="/voice"
              className="block px-3 py-2 text-base font-medium text-gray-700 hover:text-indigo-600"
            >
              Voice Therapy
            </Link>
            <div className="px-3 py-2">
              <button className="w-full bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700">
                Get Started
              </button>
            </div>
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
import React from 'react';
import { Brain } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="bg-white border-t">
      <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center space-x-2">
              <Brain className="h-8 w-8 text-indigo-600" />
              <span className="font-display text-xl font-bold text-gray-900">TherapyNest AI</span>
            </div>
            <p className="mt-4 text-gray-600 max-w-md">
              Empowering mental wellness through innovative AI-driven therapy solutions.
              Your safe space for healing and growth.
            </p>
          </div>
          
          <div>
            <h3 className="font-semibold text-gray-900">Services</h3>
            <ul className="mt-4 space-y-2">
              <li><a href="/chat" className="text-gray-600 hover:text-indigo-600">Chat Therapy</a></li>
              <li><a href="/voice" className="text-gray-600 hover:text-indigo-600">Voice Therapy</a></li>
              <li><a href="#" className="text-gray-600 hover:text-indigo-600">Resources</a></li>
            </ul>
          </div>

          <div>
            <h3 className="font-semibold text-gray-900">Company</h3>
            <ul className="mt-4 space-y-2">
              <li><a href="#" className="text-gray-600 hover:text-indigo-600">About Us</a></li>
              <li><a href="#" className="text-gray-600 hover:text-indigo-600">Privacy Policy</a></li>
              <li><a href="#" className="text-gray-600 hover:text-indigo-600">Terms of Service</a></li>
            </ul>
          </div>
        </div>
        <div className="mt-8 pt-8 border-t border-gray-200">
          <p className="text-center text-gray-500">
            © {new Date().getFullYear()} TherapyNest AI. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
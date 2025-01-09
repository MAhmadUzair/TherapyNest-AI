import React from 'react';
import { MessageSquare, Mic, Shield, Clock, Heart, Users } from 'lucide-react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div className="space-y-20">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-indigo-50 to-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center">
            <h1 className="font-display text-4xl md:text-6xl font-bold text-gray-900 mb-6">
              Your Journey to Mental Wellness
              <span className="text-indigo-600"> Starts Here</span>
            </h1>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto mb-8">
              Experience personalized therapy through advanced AI technology.
              Choose between chat and voice consultations for your comfort.
            </p>
            <div className="flex flex-col sm:flex-row justify-center gap-4">
              <Link
                to="/chat"
                className="inline-flex items-center justify-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
              >
                <MessageSquare className="w-5 h-5 mr-2" />
                Start Chat Therapy
              </Link>
              <Link
                to="/voice"
                className="inline-flex items-center justify-center px-6 py-3 border border-indigo-600 text-base font-medium rounded-md text-indigo-600 bg-white hover:bg-indigo-50"
              >
                <Mic className="w-5 h-5 mr-2" />
                Try Voice Therapy
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="bg-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="font-display text-3xl font-bold text-gray-900 mb-4">
              Why Choose TherapyNest AI?
            </h2>
            <p className="text-xl text-gray-600">
              Experience therapy that adapts to your needs
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                icon: Shield,
                title: 'Secure & Confidential',
                description: 'Your privacy is our top priority with end-to-end encryption'
              },
              {
                icon: Clock,
                title: '24/7 Availability',
                description: 'Access support whenever you need it, day or night'
              },
              {
                icon: Heart,
                title: 'Personalized Care',
                description: 'AI-driven insights tailored to your unique journey'
              }
            ].map((feature, index) => (
              <div
                key={index}
                className="bg-white p-6 rounded-lg shadow-sm border border-gray-100 hover:shadow-md transition-shadow"
              >
                <feature.icon className="w-12 h-12 text-indigo-600 mb-4" />
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  {feature.title}
                </h3>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-indigo-600 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 className="font-display text-3xl font-bold text-white mb-4">
              Ready to Start Your Healing Journey?
            </h2>
            <p className="text-xl text-indigo-100 mb-8">
              Join thousands who have found their path to mental wellness
            </p>
            <Link
              to="/chat"
              className="inline-flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-indigo-600 bg-white hover:bg-indigo-50"
            >
              Get Started Now
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
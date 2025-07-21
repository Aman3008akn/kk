import React, { useState } from 'react';
import { Mail, Gift, Truck, Shield, Headphones } from 'lucide-react';

const Newsletter: React.FC = () => {
  const [email, setEmail] = useState('');
  const [isSubscribed, setIsSubscribed] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (email) {
      setIsSubscribed(true);
      setEmail('');
      setTimeout(() => setIsSubscribed(false), 3000);
    }
  };

  const features = [
    {
      icon: Truck,
      title: 'Free Shipping',
      description: 'On orders over $99'
    },
    {
      icon: Shield,
      title: 'Secure Payment',
      description: '100% protected'
    },
    {
      icon: Gift,
      title: 'Special Offers',
      description: 'Regular discounts'
    },
    {
      icon: Headphones,
      title: '24/7 Support',
      description: 'Always here to help'
    }
  ];

  return (
    <section className="py-16 bg-gradient-to-r from-primary-600 to-primary-700">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Newsletter Signup */}
        <div className="text-center mb-16">
          <div className="max-w-2xl mx-auto">
            <Mail className="h-12 w-12 text-white mx-auto mb-6" />
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
              Stay in the Loop
            </h2>
            <p className="text-xl text-primary-100 mb-8">
              Subscribe to our newsletter and get exclusive deals, new arrivals, and insider updates
            </p>
            
            {isSubscribed ? (
              <div className="bg-green-500 text-white px-6 py-4 rounded-lg inline-flex items-center space-x-2">
                <Gift className="h-5 w-5" />
                <span className="font-medium">Thank you for subscribing!</span>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-4 max-w-md mx-auto">
                <input
                  type="email"
                  placeholder="Enter your email address"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="flex-1 px-4 py-3 rounded-lg border-0 focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-primary-600"
                  required
                />
                <button
                  type="submit"
                  className="bg-white text-primary-600 px-6 py-3 rounded-lg font-semibold hover:bg-primary-50 transition-colors duration-200"
                >
                  Subscribe
                </button>
              </form>
            )}
            
            <p className="text-primary-200 text-sm mt-4">
              No spam, unsubscribe at any time
            </p>
          </div>
        </div>

        {/* Features */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, index) => (
            <div key={index} className="text-center">
              <div className="bg-white/10 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                <feature.icon className="h-8 w-8 text-white" />
              </div>
              <h3 className="text-lg font-semibold text-white mb-2">
                {feature.title}
              </h3>
              <p className="text-primary-200">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Newsletter;
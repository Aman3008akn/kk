import React, { useState, useEffect } from 'react';
import { ChevronLeft, ChevronRight, ShoppingBag } from 'lucide-react';

const Hero: React.FC = () => {
  const [currentSlide, setCurrentSlide] = useState(0);

  const slides = [
    {
      id: 1,
      title: 'Summer Collection 2024',
      subtitle: 'Discover the latest trends',
      description: 'Up to 50% off on selected items',
      image: 'https://images.pexels.com/photos/996329/pexels-photo-996329.jpeg?auto=compress&cs=tinysrgb&w=1200',
      cta: 'Shop Now',
      bgColor: 'from-blue-600 to-purple-600'
    },
    {
      id: 2,
      title: 'Tech Innovation',
      subtitle: 'Latest gadgets & electronics',
      description: 'Free shipping on orders over $99',
      image: 'https://images.pexels.com/photos/356056/pexels-photo-356056.jpeg?auto=compress&cs=tinysrgb&w=1200',
      cta: 'Explore Tech',
      bgColor: 'from-gray-800 to-gray-600'
    },
    {
      id: 3,
      title: 'Home Essentials',
      subtitle: 'Transform your living space',
      description: 'New arrivals every week',
      image: 'https://images.pexels.com/photos/1080721/pexels-photo-1080721.jpeg?auto=compress&cs=tinysrgb&w=1200',
      cta: 'Shop Home',
      bgColor: 'from-green-600 to-teal-600'
    }
  ];

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % slides.length);
    }, 5000);
    return () => clearInterval(timer);
  }, [slides.length]);

  const nextSlide = () => {
    setCurrentSlide((prev) => (prev + 1) % slides.length);
  };

  const prevSlide = () => {
    setCurrentSlide((prev) => (prev - 1 + slides.length) % slides.length);
  };

  return (
    <section className="relative h-[600px] overflow-hidden">
      {slides.map((slide, index) => (
        <div
          key={slide.id}
          className={`absolute inset-0 transition-transform duration-500 ease-in-out ${
            index === currentSlide ? 'translate-x-0' : 
            index < currentSlide ? '-translate-x-full' : 'translate-x-full'
          }`}
        >
          <div className={`relative h-full bg-gradient-to-r ${slide.bgColor}`}>
            <div className="absolute inset-0 bg-black bg-opacity-20"></div>
            <div 
              className="absolute inset-0 bg-cover bg-center bg-no-repeat mix-blend-overlay"
              style={{ backgroundImage: `url(${slide.image})` }}
            ></div>
            
            <div className="relative h-full flex items-center">
              <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
                <div className="max-w-2xl">
                  <h1 className="text-5xl md:text-6xl font-bold text-white mb-4 animate-slide-up">
                    {slide.title}
                  </h1>
                  <p className="text-xl md:text-2xl text-white mb-2 animate-slide-up" style={{ animationDelay: '0.1s' }}>
                    {slide.subtitle}
                  </p>
                  <p className="text-lg text-white mb-8 animate-slide-up" style={{ animationDelay: '0.2s' }}>
                    {slide.description}
                  </p>
                  <button className="bg-white text-gray-900 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-gray-100 transition-colors duration-200 flex items-center space-x-2 animate-slide-up" style={{ animationDelay: '0.3s' }}>
                    <ShoppingBag className="h-5 w-5" />
                    <span>{slide.cta}</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      ))}

      {/* Navigation Arrows */}
      <button
        onClick={prevSlide}
        className="absolute left-4 top-1/2 transform -translate-y-1/2 bg-white bg-opacity-20 hover:bg-opacity-30 text-white p-2 rounded-full transition-all duration-200"
      >
        <ChevronLeft className="h-6 w-6" />
      </button>
      <button
        onClick={nextSlide}
        className="absolute right-4 top-1/2 transform -translate-y-1/2 bg-white bg-opacity-20 hover:bg-opacity-30 text-white p-2 rounded-full transition-all duration-200"
      >
        <ChevronRight className="h-6 w-6" />
      </button>

      {/* Dots Indicator */}
      <div className="absolute bottom-6 left-1/2 transform -translate-x-1/2 flex space-x-2">
        {slides.map((_, index) => (
          <button
            key={index}
            onClick={() => setCurrentSlide(index)}
            className={`w-3 h-3 rounded-full transition-all duration-200 ${
              index === currentSlide ? 'bg-white' : 'bg-white bg-opacity-50'
            }`}
          />
        ))}
      </div>
    </section>
  );
};

export default Hero;
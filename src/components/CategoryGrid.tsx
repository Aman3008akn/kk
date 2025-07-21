import React from 'react';
import { ArrowRight } from 'lucide-react';
import { categories } from '../data/mockData';

const CategoryGrid: React.FC = () => {
  return (
    <section className="py-16 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            Shop by Category
          </h2>
          <p className="text-lg text-secondary-600 max-w-2xl mx-auto">
            Explore our diverse range of product categories
          </p>
        </div>

        {/* Categories Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {categories.map((category, index) => (
            <div
              key={category.id}
              className={`group relative overflow-hidden rounded-2xl cursor-pointer transition-all duration-300 hover:shadow-xl hover:-translate-y-2 ${
                index === 0 ? 'sm:col-span-2 lg:col-span-1' : ''
              }`}
            >
              <div className="aspect-w-16 aspect-h-12 relative h-64">
                <img
                  src={category.image}
                  alt={category.name}
                  className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-black/20 to-transparent"></div>
                
                {/* Content */}
                <div className="absolute inset-0 flex flex-col justify-end p-6">
                  <h3 className="text-2xl font-bold text-white mb-2 group-hover:text-primary-300 transition-colors duration-200">
                    {category.name}
                  </h3>
                  <p className="text-white/90 mb-4">
                    {category.productCount.toLocaleString()} products
                  </p>
                  <div className="flex items-center text-white group-hover:text-primary-300 transition-colors duration-200">
                    <span className="font-medium">Shop Now</span>
                    <ArrowRight className="ml-2 h-5 w-5 transform group-hover:translate-x-1 transition-transform duration-200" />
                  </div>
                </div>

                {/* Hover Overlay */}
                <div className="absolute inset-0 bg-primary-600/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              </div>
            </div>
          ))}
        </div>

        {/* Call to Action */}
        <div className="text-center mt-12">
          <button className="btn-primary px-8 py-3 text-lg">
            View All Categories
          </button>
        </div>
      </div>
    </section>
  );
};

export default CategoryGrid;
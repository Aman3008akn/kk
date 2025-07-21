import React from 'react';
import { brands } from '../data/mockData';

const FeaturedBrands: React.FC = () => {
  return (
    <section className="py-16 bg-secondary-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            Featured Brands
          </h2>
          <p className="text-lg text-secondary-600 max-w-2xl mx-auto">
            Discover products from the world's most trusted and innovative brands
          </p>
        </div>

        {/* Brands Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
          {brands.map((brand) => (
            <div
              key={brand.id}
              className="group bg-white rounded-xl p-8 shadow-sm hover:shadow-md transition-all duration-300 cursor-pointer border border-secondary-200 hover:border-primary-300"
            >
              <div className="text-center">
                <div className="w-20 h-20 mx-auto mb-4 rounded-full overflow-hidden bg-secondary-100 group-hover:bg-primary-50 transition-colors duration-300">
                  <img
                    src={brand.logo}
                    alt={brand.name}
                    className="w-full h-full object-cover"
                  />
                </div>
                <h3 className="font-semibold text-gray-900 mb-2 group-hover:text-primary-600 transition-colors duration-200">
                  {brand.name}
                </h3>
                <p className="text-sm text-secondary-600">
                  {brand.description}
                </p>
              </div>
            </div>
          ))}
        </div>

        {/* Additional Brands Logos */}
        <div className="mt-16 pt-12 border-t border-secondary-200">
          <p className="text-center text-secondary-600 mb-8 font-medium">
            Trusted by millions of customers worldwide
          </p>
          <div className="flex flex-wrap justify-center items-center gap-8 opacity-60">
            {/* Placeholder brand logos */}
            {Array.from({ length: 8 }).map((_, index) => (
              <div
                key={index}
                className="w-24 h-12 bg-secondary-200 rounded-lg flex items-center justify-center"
              >
                <span className="text-secondary-500 font-medium text-sm">
                  Brand {index + 1}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Call to Action */}
        <div className="text-center mt-12">
          <button className="btn-primary px-8 py-3 text-lg">
            Explore All Brands
          </button>
        </div>
      </div>
    </section>
  );
};

export default FeaturedBrands;
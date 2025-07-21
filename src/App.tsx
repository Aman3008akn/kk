import React from 'react';
import Header from './components/Header';
import Hero from './components/Hero';
import CategoryGrid from './components/CategoryGrid';
import ProductGrid from './components/ProductGrid';
import FeaturedBrands from './components/FeaturedBrands';
import Testimonials from './components/Testimonials';
import Newsletter from './components/Newsletter';
import Footer from './components/Footer';
import { categories, featuredProducts, bestSellers, newArrivals } from './data/mockData';

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <main>
        <Hero />
        <CategoryGrid categories={categories} />
        <ProductGrid 
          products={featuredProducts} 
          title="Featured Products"
          subtitle="Discover our handpicked selection of premium products"
        />
        <FeaturedBrands />
        <ProductGrid 
          products={bestSellers} 
          title="Best Sellers"
          subtitle="Most popular products loved by our customers"
          className="bg-white"
        />
        <Testimonials />
        <ProductGrid 
          products={newArrivals} 
          title="New Arrivals"
          subtitle="Latest products just added to our collection"
        />
        <Newsletter />
      </main>
      <Footer />
    </div>
  );
}

export default App;
import { Product, Category, Brand, Testimonial } from '../types';

export const products: Product[] = [
  {
    id: '1',
    name: 'Premium Wireless Headphones',
    price: 299.99,
    originalPrice: 399.99,
    image: 'https://images.pexels.com/photos/3394650/pexels-photo-3394650.jpeg?auto=compress&cs=tinysrgb&w=500',
    category: 'Electronics',
    rating: 4.8,
    reviews: 1247,
    inStock: true,
    isSale: true,
    description: 'High-quality wireless headphones with noise cancellation and premium sound quality.',
    colors: ['Black', 'White', 'Silver'],
    sizes: ['One Size']
  },
  {
    id: '2',
    name: 'Smart Fitness Watch',
    price: 199.99,
    image: 'https://images.pexels.com/photos/437037/pexels-photo-437037.jpeg?auto=compress&cs=tinysrgb&w=500',
    category: 'Electronics',
    rating: 4.6,
    reviews: 892,
    inStock: true,
    isNew: true,
    description: 'Advanced fitness tracking with heart rate monitoring and GPS.',
    colors: ['Black', 'Rose Gold', 'Silver'],
    sizes: ['38mm', '42mm']
  },
  {
    id: '3',
    name: 'Designer Leather Jacket',
    price: 449.99,
    image: 'https://images.pexels.com/photos/1124465/pexels-photo-1124465.jpeg?auto=compress&cs=tinysrgb&w=500',
    category: 'Fashion',
    rating: 4.9,
    reviews: 567,
    inStock: true,
    description: 'Premium leather jacket with modern design and superior craftsmanship.',
    colors: ['Black', 'Brown', 'Tan'],
    sizes: ['S', 'M', 'L', 'XL']
  },
  {
    id: '4',
    name: 'Professional Camera Lens',
    price: 899.99,
    originalPrice: 1199.99,
    image: 'https://images.pexels.com/photos/90946/pexels-photo-90946.jpeg?auto=compress&cs=tinysrgb&w=500',
    category: 'Electronics',
    rating: 4.7,
    reviews: 324,
    inStock: true,
    isSale: true,
    description: 'Professional-grade camera lens for stunning photography.',
    colors: ['Black'],
    sizes: ['85mm', '135mm']
  },
  {
    id: '5',
    name: 'Luxury Skincare Set',
    price: 159.99,
    image: 'https://images.pexels.com/photos/3685530/pexels-photo-3685530.jpeg?auto=compress&cs=tinysrgb&w=500',
    category: 'Beauty',
    rating: 4.5,
    reviews: 1089,
    inStock: true,
    isNew: true,
    description: 'Complete skincare routine with premium natural ingredients.',
    colors: ['Natural'],
    sizes: ['Full Size', 'Travel Size']
  },
  {
    id: '6',
    name: 'Modern Office Chair',
    price: 349.99,
    image: 'https://images.pexels.com/photos/586996/pexels-photo-586996.jpeg?auto=compress&cs=tinysrgb&w=500',
    category: 'Furniture',
    rating: 4.4,
    reviews: 445,
    inStock: true,
    description: 'Ergonomic office chair with lumbar support and premium materials.',
    colors: ['Black', 'Gray', 'White'],
    sizes: ['Standard']
  },
  {
    id: '7',
    name: 'Artisan Coffee Beans',
    price: 24.99,
    image: 'https://images.pexels.com/photos/894695/pexels-photo-894695.jpeg?auto=compress&cs=tinysrgb&w=500',
    category: 'Food',
    rating: 4.8,
    reviews: 2156,
    inStock: true,
    description: 'Premium single-origin coffee beans roasted to perfection.',
    colors: ['Dark Roast', 'Medium Roast', 'Light Roast'],
    sizes: ['250g', '500g', '1kg']
  },
  {
    id: '8',
    name: 'Minimalist Desk Lamp',
    price: 89.99,
    originalPrice: 129.99,
    image: 'https://images.pexels.com/photos/1112598/pexels-photo-1112598.jpeg?auto=compress&cs=tinysrgb&w=500',
    category: 'Home',
    rating: 4.6,
    reviews: 678,
    inStock: true,
    isSale: true,
    description: 'Modern LED desk lamp with adjustable brightness and USB charging.',
    colors: ['White', 'Black', 'Silver'],
    sizes: ['Standard']
  }
];

export const categories: Category[] = [
  {
    id: '1',
    name: 'Electronics',
    image: 'https://images.pexels.com/photos/356056/pexels-photo-356056.jpeg?auto=compress&cs=tinysrgb&w=400',
    productCount: 1247
  },
  {
    id: '2',
    name: 'Fashion',
    image: 'https://images.pexels.com/photos/996329/pexels-photo-996329.jpeg?auto=compress&cs=tinysrgb&w=400',
    productCount: 892
  },
  {
    id: '3',
    name: 'Home & Garden',
    image: 'https://images.pexels.com/photos/1080721/pexels-photo-1080721.jpeg?auto=compress&cs=tinysrgb&w=400',
    productCount: 567
  },
  {
    id: '4',
    name: 'Beauty',
    image: 'https://images.pexels.com/photos/3685530/pexels-photo-3685530.jpeg?auto=compress&cs=tinysrgb&w=400',
    productCount: 324
  },
  {
    id: '5',
    name: 'Sports',
    image: 'https://images.pexels.com/photos/863988/pexels-photo-863988.jpeg?auto=compress&cs=tinysrgb&w=400',
    productCount: 445
  },
  {
    id: '6',
    name: 'Books',
    image: 'https://images.pexels.com/photos/159711/books-bookstore-book-reading-159711.jpeg?auto=compress&cs=tinysrgb&w=400',
    productCount: 1089
  }
];

export const brands: Brand[] = [
  {
    id: '1',
    name: 'TechPro',
    logo: 'https://images.pexels.com/photos/267350/pexels-photo-267350.jpeg?auto=compress&cs=tinysrgb&w=200',
    description: 'Leading technology brand'
  },
  {
    id: '2',
    name: 'StyleCo',
    logo: 'https://images.pexels.com/photos/298863/pexels-photo-298863.jpeg?auto=compress&cs=tinysrgb&w=200',
    description: 'Premium fashion brand'
  },
  {
    id: '3',
    name: 'HomeEssentials',
    logo: 'https://images.pexels.com/photos/1080721/pexels-photo-1080721.jpeg?auto=compress&cs=tinysrgb&w=200',
    description: 'Quality home products'
  },
  {
    id: '4',
    name: 'BeautyLux',
    logo: 'https://images.pexels.com/photos/3685530/pexels-photo-3685530.jpeg?auto=compress&cs=tinysrgb&w=200',
    description: 'Luxury beauty products'
  }
];

export const testimonials: Testimonial[] = [
  {
    id: '1',
    name: 'Sarah Johnson',
    avatar: 'https://images.pexels.com/photos/774909/pexels-photo-774909.jpeg?auto=compress&cs=tinysrgb&w=100',
    rating: 5,
    comment: 'Amazing quality products and fast shipping. Highly recommend!',
    location: 'New York, NY'
  },
  {
    id: '2',
    name: 'Michael Chen',
    avatar: 'https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg?auto=compress&cs=tinysrgb&w=100',
    rating: 5,
    comment: 'Great customer service and excellent product selection.',
    location: 'San Francisco, CA'
  },
  {
    id: '3',
    name: 'Emily Davis',
    avatar: 'https://images.pexels.com/photos/415829/pexels-photo-415829.jpeg?auto=compress&cs=tinysrgb&w=100',
    rating: 4,
    comment: 'Love the variety and quality. Will definitely shop here again!',
    location: 'Austin, TX'
  }
];
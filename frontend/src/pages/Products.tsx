import React, { useState } from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import api from '../services/api';
import Card from '../components/Card';
import Button from '../components/Button';
import Badge from '../components/Badge';
import toast from 'react-hot-toast';

function Products() {
  const [products, setProducts] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [newProduct, setNewProduct] = useState({
    id: '', name: '', category: '', description: '',
    features: '', pricing: '', sla: '', compliance: '', case_studies: ''
  });
  const [showForm, setShowForm] = useState(false);

  // Fetch products
  const productsQuery = useQuery({
    queryKey: ['products'],
    queryFn: () => api.get('/products').then(r => r.data.products || []),
  });

  // Add product mutation
  const addMutation = useMutation({
    mutationFn: (product) => api.post('/products/add', product),
    onSuccess: () => {
      toast.success('Product added successfully!');
      setNewProduct({ id: '', name: '', category: '', description: '', features: '', pricing: '', sla: '', compliance: '', case_studies: '' });
      setShowForm(false);
      productsQuery.refetch();
    },
    onError: (error) => {
      toast.error('Error adding product: ' + error.message);
    },
  });

  // Search products mutation
  const searchMutation = useMutation({
    mutationFn: (query) => api.post('/products/search', { query, n_results: 10 }),
    onSuccess: (response) => {
      // Results would be in response.data.results
    },
  });

  const handleAddProduct = () => {
    if (!newProduct.id || !newProduct.name) {
      toast.error('ID and Name are required');
      return;
    }
    addMutation.mutate(newProduct);
  };

  React.useEffect(() => {
    if (productsQuery.data) setProducts(productsQuery.data);
  }, [productsQuery.data]);

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Product Management</h1>
          <p className="text-gray-600 dark:text-gray-400 mt-2">Manage product knowledge base</p>
        </div>
        <Button onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : '+ Add Product'}
        </Button>
      </div>

      {/* Add Product Form */}
      {showForm && (
        <Card>
          <div className="p-6">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Add New Product</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <input
                type="text"
                placeholder="Product ID"
                value={newProduct.id}
                onChange={(e) => setNewProduct({ ...newProduct, id: e.target.value })}
                className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
              />
              <input
                type="text"
                placeholder="Product Name"
                value={newProduct.name}
                onChange={(e) => setNewProduct({ ...newProduct, name: e.target.value })}
                className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
              />
              <input
                type="text"
                placeholder="Category"
                value={newProduct.category}
                onChange={(e) => setNewProduct({ ...newProduct, category: e.target.value })}
                className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
              />
              <input
                type="text"
                placeholder="Pricing"
                value={newProduct.pricing}
                onChange={(e) => setNewProduct({ ...newProduct, pricing: e.target.value })}
                className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
              />
              <textarea
                placeholder="Description"
                value={newProduct.description}
                onChange={(e) => setNewProduct({ ...newProduct, description: e.target.value })}
                className="col-span-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
              />
              <textarea
                placeholder="Features (comma-separated)"
                value={newProduct.features}
                onChange={(e) => setNewProduct({ ...newProduct, features: e.target.value })}
                className="col-span-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
              />
            </div>
            <Button onClick={handleAddProduct} loading={addMutation.isPending} className="w-full mt-4">
              Add Product
            </Button>
          </div>
        </Card>
      )}

      {/* Products List */}
      <div className="space-y-4">
        <div className="mb-4">
          <input
            type="text"
            placeholder="Search products..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
          />
        </div>

        {products.map((product) => (
          <Card key={product.id}>
            <div className="p-6">
              <div className="flex justify-between items-start mb-2">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white">{product.name}</h3>
                  <Badge variant="secondary" className="mt-2">{product.category}</Badge>
                </div>
                <span className="text-sm font-medium text-gray-500 dark:text-gray-400">{product.id}</span>
              </div>
              <p className="text-sm text-gray-600 dark:text-gray-400 mt-3">{product.description}</p>
              <div className="mt-4 grid grid-cols-2 gap-4 text-sm">
                <div>
                  <p className="font-medium text-gray-700 dark:text-gray-300">Pricing</p>
                  <p className="text-gray-600 dark:text-gray-400">{product.pricing}</p>
                </div>
                <div>
                  <p className="font-medium text-gray-700 dark:text-gray-300">Compliance</p>
                  <p className="text-gray-600 dark:text-gray-400">{product.compliance}</p>
                </div>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}

export default Products;

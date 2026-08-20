"use client";

import { useEffect, useState } from "react";

type Product = {
  id: string;
  name: string;
  category: string;
  price: number;
  dimensions: {
    width: number;
    depth: number;
    height: number;
  };
  material: string;
  color: string;
  style: string;
};

export default function Home() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("http://localhost:8000/api/products")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch products");
        }
        return response.json();
      })
      .then((data) => {
        setProducts(data);
        setLoading(false);
      })
      .catch(() => {
        setError("Unable to connect to VirtualShop AI backend.");
        setLoading(false);
      });
  }, []);

  return (
    <main className="min-h-screen bg-slate-50 text-slate-900">
      {/* Header */}
      <header className="border-b bg-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <div>
            <h1 className="text-2xl font-bold tracking-tight">
              VirtualShop AI
            </h1>
            <p className="text-sm text-slate-500">
              Visualize before you buy
            </p>
          </div>

          <button className="rounded-lg border px-4 py-2 text-sm font-medium hover:bg-slate-50">
            My Studio
          </button>
        </div>
      </header>

      {/* Hero */}
      <section className="mx-auto max-w-7xl px-6 pb-10 pt-14">
        <div className="max-w-3xl">
          <p className="mb-3 text-sm font-semibold uppercase tracking-widest text-indigo-600">
            AI-Powered Virtual Shopping
          </p>

          <h2 className="text-4xl font-bold tracking-tight md:text-5xl">
            See how it fits before you buy.
          </h2>

          <p className="mt-5 max-w-2xl text-lg leading-8 text-slate-600">
            Upload your room and visualize furniture in your actual space.
            VirtualShop AI helps you understand fit, style, and compatibility
            before making a purchase.
          </p>
        </div>
      </section>

      {/* Products */}
      <section className="mx-auto max-w-7xl px-6 pb-16">
        <div className="mb-6 flex items-end justify-between">
          <div>
            <h3 className="text-2xl font-bold">Explore furniture</h3>
            <p className="mt-1 text-sm text-slate-500">
              Select a product to visualize it in your space.
            </p>
          </div>

          <span className="text-sm text-slate-500">
            {products.length} products
          </span>
        </div>

        {loading && (
          <div className="rounded-xl border bg-white p-10 text-center">
            <p className="text-slate-500">Loading products...</p>
          </div>
        )}

        {error && (
          <div className="rounded-xl border border-red-200 bg-red-50 p-6 text-red-700">
            {error}
          </div>
        )}

        {!loading && !error && (
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {products.map((product) => (
              <article
                key={product.id}
                className="overflow-hidden rounded-2xl border bg-white shadow-sm transition hover:-translate-y-1 hover:shadow-lg"
              >
                {/* Product visual placeholder */}
                <div className="flex h-52 items-center justify-center bg-slate-100">
                  <div className="text-center">
                    <div className="text-5xl">🛋️</div>
                    <p className="mt-3 text-xs text-slate-400">
                      Product preview
                    </p>
                  </div>
                </div>

                <div className="p-5">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-semibold uppercase tracking-wide text-indigo-600">
                      {product.category}
                    </span>

                    <span className="text-xs text-slate-400">
                      {product.style}
                    </span>
                  </div>

                  <h4 className="mt-2 text-lg font-semibold">
                    {product.name}
                  </h4>

                  <p className="mt-2 text-sm text-slate-500">
                    {product.material} · {product.color}
                  </p>

                  <p className="mt-4 text-xl font-bold">
                    ₹{product.price.toLocaleString("en-IN")}
                  </p>

                  <div className="mt-4 rounded-lg bg-slate-50 p-3 text-xs text-slate-500">
                    <p className="font-medium text-slate-700">Dimensions</p>
                    <p className="mt-1">
                      {product.dimensions.width} ×{" "}
                      {product.dimensions.depth} ×{" "}
                      {product.dimensions.height} cm
                    </p>
                  </div>

                  <button className="mt-5 w-full rounded-xl bg-slate-900 px-4 py-3 text-sm font-semibold text-white transition hover:bg-slate-700">
                    Visualize in my space
                  </button>
                </div>
              </article>
            ))}
          </div>
        )}
      </section>
    </main>
  );
}
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
  image?: string;
};

export default function Home() {
  const [products, setProducts] = useState<Product[]>([]);
  const [selectedProducts, setSelectedProducts] = useState<string[]>([]);
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
      .then((data: Product[]) => {
        setProducts(data);
        setLoading(false);
      })
      .catch(() => {
        setError(
          "Unable to connect to VirtualShop AI backend."
        );
        setLoading(false);
      });
  }, []);

  const toggleCompare = (productId: string) => {
    setSelectedProducts((current) => {
      if (current.includes(productId)) {
        return current.filter((id) => id !== productId);
      }

      if (current.length >= 3) {
        return current;
      }

      return [...current, productId];
    });
  };

  const compareUrl =
    selectedProducts.length >= 2
      ? `/compare?products=${selectedProducts.join(",")}`
      : "#";

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

          <a
            href="/studio"
            className="rounded-lg border px-4 py-2 text-sm font-medium hover:bg-slate-50"
          >
            My Studio
          </a>
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
            Upload your room and visualize furniture in your actual
            space. VirtualShop AI helps you understand fit, style,
            and compatibility before making a purchase.
          </p>
        </div>
      </section>

      {/* Products */}
      <section className="mx-auto max-w-7xl px-6 pb-16">
        <div className="mb-6 flex items-end justify-between">
          <div>
            <h3 className="text-2xl font-bold">
              Explore furniture
            </h3>

            <p className="mt-1 text-sm text-slate-500">
              Select a product to visualize it or compare products.
            </p>
          </div>

          <span className="text-sm text-slate-500">
            {products.length} products
          </span>
        </div>

        {/* Compare Bar */}
        {selectedProducts.length > 0 && (
          <div className="mb-6 flex flex-col gap-4 rounded-2xl border bg-white p-5 shadow-sm sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p className="font-semibold">
                {selectedProducts.length} product
                {selectedProducts.length !== 1 ? "s" : ""} selected
              </p>

              <p className="mt-1 text-sm text-slate-500">
                Select 2 or 3 products to compare them side by side.
              </p>
            </div>

            <div className="flex gap-3">
              <button
                onClick={() => setSelectedProducts([])}
                className="rounded-xl border px-4 py-3 text-sm font-semibold hover:bg-slate-50"
              >
                Clear
              </button>

              <a
                href={compareUrl}
                className={`rounded-xl px-5 py-3 text-sm font-semibold text-white ${
                  selectedProducts.length >= 2
                    ? "bg-indigo-600 hover:bg-indigo-500"
                    : "pointer-events-none bg-slate-300"
                }`}
              >
                Compare selected
              </a>
            </div>
          </div>
        )}

        {/* Loading */}
        {loading && (
          <div className="rounded-xl border bg-white p-10 text-center">
            <p className="text-slate-500">
              Loading products...
            </p>
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="rounded-xl border border-red-200 bg-red-50 p-6 text-red-700">
            {error}
          </div>
        )}

        {/* Product Grid */}
        {!loading && !error && (
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {products.map((product) => {
              const isSelected = selectedProducts.includes(
                product.id
              );

              const comparisonLimitReached =
                selectedProducts.length >= 3 &&
                !isSelected;

              return (
                <article
                  key={product.id}
                  className={`overflow-hidden rounded-2xl border bg-white shadow-sm transition hover:-translate-y-1 hover:shadow-lg ${
                    isSelected
                      ? "border-indigo-500 ring-2 ring-indigo-100"
                      : ""
                  }`}
                >
                  {/* Product Image */}
                  <div className="flex h-52 items-center justify-center overflow-hidden bg-slate-100">
                    {product.image ? (
                      <img
                        src={product.image}
                        alt={product.name}
                        className="h-full w-full object-contain"
                      />
                    ) : (
                      <div className="text-center">
                        <div className="text-5xl">
                          🛋️
                        </div>

                        <p className="mt-3 text-xs text-slate-400">
                          Image coming soon
                        </p>
                      </div>
                    )}
                  </div>

                  {/* Product Details */}
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

                    {/* Dimensions */}
                    <div className="mt-4 rounded-lg bg-slate-50 p-3 text-xs text-slate-500">
                      <p className="font-medium text-slate-700">
                        Dimensions
                      </p>

                      <p className="mt-1">
                        {product.dimensions.width} ×{" "}
                        {product.dimensions.depth} ×{" "}
                        {product.dimensions.height} cm
                      </p>
                    </div>

                    {/* Compare Checkbox */}
                    <label
                      className={`mt-4 flex cursor-pointer items-center gap-3 rounded-xl border p-3 ${
                        comparisonLimitReached
                          ? "cursor-not-allowed opacity-50"
                          : "hover:bg-slate-50"
                      }`}
                    >
                      <input
                        type="checkbox"
                        checked={isSelected}
                        disabled={comparisonLimitReached}
                        onChange={() =>
                          toggleCompare(product.id)
                        }
                        className="h-4 w-4 accent-indigo-600"
                      />

                      <span className="text-sm font-medium">
                        Compare
                      </span>
                    </label>

                    {/* Visualization Button */}
                    <a
                      href={`/studio?product=${product.id}`}
                      className="mt-4 block w-full rounded-xl bg-slate-900 px-4 py-3 text-center text-sm font-semibold text-white transition hover:bg-slate-700"
                    >
                      Visualize in my space
                    </a>
                  </div>
                </article>
              );
            })}
          </div>
        )}
      </section>
    </main>
  );
}
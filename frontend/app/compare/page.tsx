"use client";

import { useEffect, useMemo, useState } from "react";

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

type Tradeoff = {
  product: string;
  advantages: string[];
  tradeoffs: string[];
};

type AIComparison = {
  summary: string;
  best_value: string;
  best_for_small_spaces: string;
  best_style_match: string;
  recommendation: string;
  reasoning: string;
  tradeoffs: Tradeoff[];
};

export default function ComparePage() {
  const [products, setProducts] = useState<Product[]>([]);

  const [loading, setLoading] = useState(true);
  const [aiLoading, setAiLoading] = useState(false);

  const [error, setError] = useState("");
  const [aiError, setAiError] = useState("");

  const [aiComparison, setAiComparison] =
    useState<AIComparison | null>(null);

  useEffect(() => {
    async function loadComparison() {
      try {
        setLoading(true);
        setError("");
        setAiError("");

        // --------------------------------------------------
        // 1. Read selected product IDs from URL
        // --------------------------------------------------

        const params = new URLSearchParams(
          window.location.search
        );

        const selectedIdsParam =
          params.get("products");

        if (!selectedIdsParam) {
          throw new Error(
            "No products selected for comparison."
          );
        }

        const selectedIds =
          selectedIdsParam
            .split(",")
            .filter(Boolean);

        if (selectedIds.length < 2) {
          throw new Error(
            "Please select at least two products to compare."
          );
        }

        // --------------------------------------------------
        // 2. Load products from backend
        // --------------------------------------------------

        const productsResponse = await fetch(
          "http://localhost:8000/api/products"
        );

        if (!productsResponse.ok) {
          throw new Error(
            "Failed to load products from backend."
          );
        }

        const allProducts: Product[] =
          await productsResponse.json();

        // --------------------------------------------------
        // 3. Find selected products
        // --------------------------------------------------

        const selectedProducts =
          allProducts.filter((product) =>
            selectedIds.includes(product.id)
          );

        if (
          selectedProducts.length !==
          selectedIds.length
        ) {
          throw new Error(
            "One or more selected products were not found."
          );
        }

        setProducts(selectedProducts);
        setLoading(false);

        // --------------------------------------------------
        // 4. Call AI comparison endpoint
        // --------------------------------------------------

        setAiLoading(true);

        const comparisonResponse =
          await fetch(
            "http://localhost:8000/api/compare",
            {
              method: "POST",

              headers: {
                "Content-Type": "application/json",
              },

              // FastAPI expects:
              //
              // {
              //   "product_ids": [...]
              // }
              //
              body: JSON.stringify({
                product_ids: selectedIds,
              }),
            }
          );

        // --------------------------------------------------
        // 5. Read backend response
        // --------------------------------------------------

        const comparisonData =
          await comparisonResponse.json();

        // --------------------------------------------------
        // 6. Handle HTTP errors
        // --------------------------------------------------

        if (!comparisonResponse.ok) {
          const backendMessage =
            comparisonData?.detail?.[0]?.msg;

          setAiError(
            backendMessage ||
              "AI comparison request failed."
          );

          return;
        }

        // --------------------------------------------------
        // 7. Handle application-level errors
        // --------------------------------------------------

        if (!comparisonData.success) {
          setAiError(
            comparisonData.message ||
              "Unable to generate AI comparison."
          );

          return;
        }

        // --------------------------------------------------
        // 8. Store AI comparison
        // --------------------------------------------------

        setAiComparison(
          comparisonData.comparison
        );

      } catch (err) {
        const message =
          err instanceof Error
            ? err.message
            : "Unable to load comparison.";

        setError(message);
        setLoading(false);
      } finally {
        setAiLoading(false);
      }
    }

    loadComparison();
  }, []);

  // --------------------------------------------------------
  // Lowest price
  // --------------------------------------------------------

  const lowestPrice = useMemo(() => {
    if (products.length === 0) {
      return null;
    }

    return Math.min(
      ...products.map(
        (product) => product.price
      )
    );
  }, [products]);

  // --------------------------------------------------------
  // Loading
  // --------------------------------------------------------

  if (loading) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-slate-50">
        <p className="text-slate-500">
          Loading comparison...
        </p>
      </main>
    );
  }

  // --------------------------------------------------------
  // Main comparison error
  // --------------------------------------------------------

  if (error) {
    return (
      <main className="min-h-screen bg-slate-50 px-6 py-16">
        <div className="mx-auto max-w-3xl rounded-2xl border bg-white p-10 text-center shadow-sm">

          <h1 className="text-2xl font-bold">
            Unable to compare products
          </h1>

          <p className="mt-3 text-slate-500">
            {error}
          </p>

          <a
            href="/"
            className="mt-6 inline-block rounded-xl bg-slate-900 px-5 py-3 text-sm font-semibold text-white hover:bg-slate-700"
          >
            Back to catalog
          </a>

        </div>
      </main>
    );
  }

  // --------------------------------------------------------
  // Main UI
  // --------------------------------------------------------

  return (
    <main className="min-h-screen bg-slate-50 text-slate-900">

      {/* -------------------------------------------------- */}
      {/* Header */}
      {/* -------------------------------------------------- */}

      <header className="border-b bg-white">

        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">

          <div>

            <h1 className="text-2xl font-bold tracking-tight">
              VirtualShop AI
            </h1>

            <p className="text-sm text-slate-500">
              AI-powered product comparison
            </p>

          </div>

          <a
            href="/"
            className="rounded-lg border px-4 py-2 text-sm font-medium hover:bg-slate-50"
          >
            Back to catalog
          </a>

        </div>

      </header>


      {/* -------------------------------------------------- */}
      {/* Main */}
      {/* -------------------------------------------------- */}

      <section className="mx-auto max-w-7xl px-6 py-12">

        {/* Heading */}

        <div className="mb-10">

          <p className="text-sm font-semibold uppercase tracking-widest text-indigo-600">
            Compare furniture
          </p>

          <h2 className="mt-2 text-4xl font-bold tracking-tight">
            Find the right product for your space.
          </h2>

          <p className="mt-3 max-w-2xl text-slate-500">
            Compare product specifications and get
            an AI-powered recommendation based only
            on the available product data.
          </p>

        </div>


        {/* ------------------------------------------------ */}
        {/* AI Loading */}
        {/* ------------------------------------------------ */}

        {aiLoading && (

          <div className="mb-8 rounded-2xl border border-indigo-100 bg-indigo-50 p-6">

            <div className="flex items-center gap-3">

              <div className="h-5 w-5 animate-spin rounded-full border-2 border-indigo-200 border-t-indigo-600" />

              <div>

                <p className="font-semibold text-indigo-900">
                  AI is comparing the products...
                </p>

                <p className="mt-1 text-sm text-indigo-700">
                  Gemini is analyzing price,
                  dimensions, material and style.
                </p>

              </div>

            </div>

          </div>

        )}


        {/* ------------------------------------------------ */}
        {/* AI Error */}
        {/* ------------------------------------------------ */}

        {aiError && (

          <div className="mb-8 rounded-2xl border border-red-200 bg-red-50 p-5">

            <p className="font-semibold text-red-800">
              AI comparison unavailable
            </p>

            <p className="mt-1 text-sm text-red-700">
              {aiError}
            </p>

          </div>

        )}


        {/* ------------------------------------------------ */}
        {/* AI Recommendation */}
        {/* ------------------------------------------------ */}

        {aiComparison && (

          <div className="mb-8 rounded-2xl border border-indigo-100 bg-white p-6 shadow-sm">

            {/* Recommendation header */}

            <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">

              <div>

                <p className="text-sm font-semibold uppercase tracking-widest text-indigo-600">
                  AI Recommendation
                </p>

                <h3 className="mt-2 text-2xl font-bold">
                  {aiComparison.recommendation}
                </h3>

                <p className="mt-3 max-w-3xl leading-7 text-slate-600">
                  {aiComparison.reasoning}
                </p>

              </div>


              <div className="rounded-xl bg-indigo-50 px-5 py-4 text-center">

                <p className="text-xs font-semibold uppercase tracking-wide text-indigo-600">
                  Recommended
                </p>

                <p className="mt-1 font-bold text-indigo-900">
                  {aiComparison.recommendation}
                </p>

              </div>

            </div>


            {/* AI decision categories */}

            <div className="mt-6 grid gap-4 md:grid-cols-3">

              <div className="rounded-xl bg-slate-50 p-4">

                <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
                  Best Value
                </p>

                <p className="mt-2 font-bold">
                  {aiComparison.best_value}
                </p>

              </div>


              <div className="rounded-xl bg-slate-50 p-4">

                <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
                  Best for Small Spaces
                </p>

                <p className="mt-2 font-bold">
                  {aiComparison.best_for_small_spaces}
                </p>

              </div>


              <div className="rounded-xl bg-slate-50 p-4">

                <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
                  Best Style Match
                </p>

                <p className="mt-2 font-bold">
                  {aiComparison.best_style_match}
                </p>

              </div>

            </div>


            {/* AI Summary */}

            <div className="mt-6 rounded-xl border bg-slate-50 p-5">

              <p className="text-xs font-semibold uppercase tracking-wide text-indigo-600">
                AI Summary
              </p>

              <p className="mt-2 leading-7 text-slate-600">
                {aiComparison.summary}
              </p>

            </div>


            {/* Tradeoffs */}

            {aiComparison.tradeoffs &&
              aiComparison.tradeoffs.length > 0 && (

                <div className="mt-6">

                  <h4 className="text-lg font-bold">
                    Product trade-offs
                  </h4>

                  <div className="mt-4 grid gap-4 md:grid-cols-2">

                    {aiComparison.tradeoffs.map(
                      (tradeoff) => (

                        <div
                          key={tradeoff.product}
                          className="rounded-xl border p-5"
                        >

                          <h5 className="font-bold">
                            {tradeoff.product}
                          </h5>


                          {/* Advantages */}

                          <div className="mt-4">

                            <p className="text-sm font-semibold text-green-700">
                              Advantages
                            </p>

                            <ul className="mt-2 space-y-1">

                              {tradeoff.advantages.map(
                                (advantage, index) => (

                                  <li
                                    key={index}
                                    className="text-sm text-slate-600"
                                  >
                                    • {advantage}
                                  </li>

                                )
                              )}

                            </ul>

                          </div>


                          {/* Trade-offs */}

                          <div className="mt-4">

                            <p className="text-sm font-semibold text-amber-700">
                              Trade-offs
                            </p>

                            <ul className="mt-2 space-y-1">

                              {tradeoff.tradeoffs.map(
                                (item, index) => (

                                  <li
                                    key={index}
                                    className="text-sm text-slate-600"
                                  >
                                    • {item}
                                  </li>

                                )
                              )}

                            </ul>

                          </div>

                        </div>

                      )
                    )}

                  </div>

                </div>

              )}

          </div>

        )}


        {/* ------------------------------------------------ */}
        {/* Product Comparison */}
        {/* ------------------------------------------------ */}

        <div className="overflow-x-auto rounded-2xl border bg-white shadow-sm">

          <div
            className="grid min-w-[800px]"
            style={{
              gridTemplateColumns:
                `180px repeat(${products.length}, minmax(220px, 1fr))`,
            }}
          >

            {/* Product */}

            <ComparisonLabel label="Product" />

            {products.map((product) => (

              <div
                key={product.id}
                className="border-b p-5"
              >

                <div className="flex h-48 items-center justify-center overflow-hidden rounded-xl bg-slate-100">

                  {product.image ? (

                    <img
                      src={product.image}
                      alt={product.name}
                      className="h-full w-full object-contain"
                    />

                  ) : (

                    <span className="text-5xl">
                      🪑
                    </span>

                  )}

                </div>


                <h3 className="mt-4 text-lg font-bold">
                  {product.name}
                </h3>

                <p className="mt-1 text-sm text-indigo-600">
                  {product.category}
                </p>

              </div>

            ))}


            {/* Price */}

            <ComparisonLabel label="Price" />

            {products.map((product) => (

              <ComparisonValue key={product.id}>

                <span className="text-xl font-bold">
                  ₹{product.price.toLocaleString("en-IN")}
                </span>

                {product.price === lowestPrice && (

                  <span className="ml-2 rounded-full bg-green-100 px-2 py-1 text-xs font-semibold text-green-700">
                    Lowest price
                  </span>

                )}

              </ComparisonValue>

            ))}


            {/* Category */}

            <ComparisonLabel label="Category" />

            {products.map((product) => (

              <ComparisonValue key={product.id}>
                {product.category}
              </ComparisonValue>

            ))}


            {/* Material */}

            <ComparisonLabel label="Material" />

            {products.map((product) => (

              <ComparisonValue key={product.id}>
                {product.material}
              </ComparisonValue>

            ))}


            {/* Color */}

            <ComparisonLabel label="Color" />

            {products.map((product) => (

              <ComparisonValue key={product.id}>
                {product.color}
              </ComparisonValue>

            ))}


            {/* Style */}

            <ComparisonLabel label="Style" />

            {products.map((product) => (

              <ComparisonValue key={product.id}>
                {product.style}
              </ComparisonValue>

            ))}


            {/* Width */}

            <ComparisonLabel label="Width" />

            {products.map((product) => (

              <ComparisonValue key={product.id}>
                {product.dimensions.width} cm
              </ComparisonValue>

            ))}


            {/* Depth */}

            <ComparisonLabel label="Depth" />

            {products.map((product) => (

              <ComparisonValue key={product.id}>
                {product.dimensions.depth} cm
              </ComparisonValue>

            ))}


            {/* Height */}

            <ComparisonLabel label="Height" />

            {products.map((product) => (

              <ComparisonValue key={product.id}>
                {product.dimensions.height} cm
              </ComparisonValue>

            ))}


            {/* Full Dimensions */}

            <ComparisonLabel label="Dimensions" />

            {products.map((product) => (

              <ComparisonValue key={product.id}>

                {product.dimensions.width} ×{" "}
                {product.dimensions.depth} ×{" "}
                {product.dimensions.height} cm

              </ComparisonValue>

            ))}


            {/* Action */}

            <ComparisonLabel label="Action" />

            {products.map((product) => (

              <ComparisonValue key={product.id}>

                <a
                  href={`/studio?product=${product.id}`}
                  className="block w-full rounded-xl bg-slate-900 px-4 py-3 text-center text-sm font-semibold text-white hover:bg-slate-700"
                >
                  Visualize in my space
                </a>

              </ComparisonValue>

            ))}

          </div>

        </div>


        {/* ------------------------------------------------ */}
        {/* Explanation */}
        {/* ------------------------------------------------ */}

        <div className="mt-8 rounded-2xl border bg-white p-6">

          <h3 className="text-lg font-bold">
            What should you consider?
          </h3>

          <div className="mt-4 grid gap-4 md:grid-cols-3">

            <div>

              <p className="font-semibold">
                📐 Dimensions
              </p>

              <p className="mt-1 text-sm leading-6 text-slate-500">
                Check whether the furniture fits your
                available space.
              </p>

            </div>


            <div>

              <p className="font-semibold">
                🎨 Style & material
              </p>

              <p className="mt-1 text-sm leading-6 text-slate-500">
                Compare the visual character and
                construction of each product.
              </p>

            </div>


            <div>

              <p className="font-semibold">
                💰 Price
              </p>

              <p className="mt-1 text-sm leading-6 text-slate-500">
                Compare the cost before deciding
                which product to visualize.
              </p>

            </div>

          </div>

        </div>

      </section>

    </main>
  );
}


// ----------------------------------------------------------
// Comparison label
// ----------------------------------------------------------

function ComparisonLabel({
  label,
}: {
  label: string;
}) {
  return (
    <div className="border-b border-r bg-slate-50 p-5">
      <span className="text-sm font-semibold text-slate-500">
        {label}
      </span>
    </div>
  );
}


// ----------------------------------------------------------
// Comparison value
// ----------------------------------------------------------

function ComparisonValue({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="border-b p-5">
      {children}
    </div>
  );
}
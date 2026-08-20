"use client";

import { ChangeEvent, useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";

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

export default function StudioPage() {
  const searchParams = useSearchParams();
  const productId = searchParams.get("product");

  const [product, setProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState(true);

  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [visualization, setVisualization] = useState<string | null>(null);
  const [imageFile, setImageFile] = useState<File | null>(null);

  const [analyzing, setAnalyzing] = useState(false);

  const [analysis, setAnalysis] = useState<{
    fit_score: number;
    style_match: number;
    space_utilization: number;
    recommendation: string;
  } | null>(null);

  const [error, setError] = useState("");

  useEffect(() => {
    if (!productId) {
      setLoading(false);
      return;
    }

    fetch("http://localhost:8000/api/products")
      .then((response) => response.json())
      .then((products: Product[]) => {
        const selectedProduct = products.find(
          (item) => item.id === productId
        );

        setProduct(selectedProduct ?? null);
        setLoading(false);
      })
      .catch(() => {
        setLoading(false);
      });
  }, [productId]);

  function handleImageUpload(
    event: ChangeEvent<HTMLInputElement>
  ) {
    const file = event.target.files?.[0];

    if (!file) {
      return;
    }

    const previewUrl = URL.createObjectURL(file);

    setImageFile(file);
    setImagePreview(previewUrl);
    setVisualization(null);
    setAnalysis(null);
    setError("");
  }

  async function handleAnalyze() {
    if (!imageFile || !product) {
      return;
    }

    setAnalyzing(true);
    setError("");
    setAnalysis(null);
    setVisualization(null);

    try {
      const formData = new FormData();

      formData.append("room_image", imageFile);
      formData.append("product_id", product.id);

      const response = await fetch(
        "http://localhost:8000/api/visualize",
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error("Analysis request failed");
      }

      const data = await response.json();

      if (!data.success) {
        throw new Error(
          data.message || "Unable to analyze space"
        );
      }

      setAnalysis(data.analysis);
      setVisualization(data.visualization);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Something went wrong while analyzing the space."
      );
    } finally {
      setAnalyzing(false);
    }
  }

  if (loading) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-slate-50">
        <p className="text-slate-500">
          Loading studio...
        </p>
      </main>
    );
  }

  if (!product) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-slate-50 px-6">
        <div className="rounded-2xl border bg-white p-8 text-center shadow-sm">

          <h1 className="text-xl font-bold">
            No product selected
          </h1>

          <p className="mt-2 text-sm text-slate-500">
            Please return to the catalog and select a product first.
          </p>

          <a
            href="/"
            className="mt-6 inline-block rounded-xl bg-slate-900 px-5 py-3 text-sm font-semibold text-white"
          >
            Back to catalog
          </a>

        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-slate-50 text-slate-900">

      {/* Header */}
      <header className="border-b bg-white">

        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">

          <div>

            <h1 className="text-2xl font-bold">
              VirtualShop AI
            </h1>

            <p className="text-sm text-slate-500">
              AI Visualization Studio
            </p>

          </div>

          <a
            href="/"
            className="rounded-lg border px-4 py-2 text-sm font-medium hover:bg-slate-50"
          >
            ← Back to catalog
          </a>

        </div>

      </header>


      <section className="mx-auto max-w-7xl px-6 py-10">

        {/* Title */}
        <div className="mb-8">

          <p className="text-sm font-semibold uppercase tracking-widest text-indigo-600">
            Studio
          </p>

          <h2 className="mt-2 text-4xl font-bold tracking-tight">
            Visualize your product in your space
          </h2>

          <p className="mt-3 max-w-2xl text-slate-600">
            Upload a photo of your room and see how your selected
            furniture could look in the space.
          </p>

        </div>


        <div className="grid gap-8 lg:grid-cols-[1fr_360px]">

          {/* Upload area */}
          <div className="rounded-2xl border bg-white p-6 shadow-sm">

            <h3 className="text-lg font-bold">
              1. Upload your room
            </h3>

            <p className="mt-1 text-sm text-slate-500">
              Use a clear photo showing the area where you want to
              place the furniture.
            </p>


            <div className="mt-6">

              {imagePreview ? (

                <div className="relative overflow-hidden rounded-2xl border bg-slate-100">

                  <img
                    src={imagePreview}
                    alt="Uploaded room"
                    className="max-h-[520px] w-full object-contain"
                  />


                  <label className="absolute bottom-4 right-4 cursor-pointer rounded-lg bg-white px-4 py-2 text-sm font-semibold shadow hover:bg-slate-50">

                    Change image

                    <input
                      type="file"
                      accept="image/*"
                      onChange={handleImageUpload}
                      className="hidden"
                    />

                  </label>

                </div>

              ) : (

                <label className="flex min-h-[420px] cursor-pointer flex-col items-center justify-center rounded-2xl border-2 border-dashed border-slate-300 bg-slate-50 px-6 text-center transition hover:border-indigo-400 hover:bg-indigo-50">

                  <div className="text-6xl">
                    📷
                  </div>

                  <h4 className="mt-5 text-lg font-semibold">
                    Upload a room photo
                  </h4>

                  <p className="mt-2 max-w-md text-sm text-slate-500">
                    Drag and drop your image here, or click to browse
                    your device.
                  </p>

                  <span className="mt-5 rounded-xl bg-slate-900 px-5 py-3 text-sm font-semibold text-white">
                    Choose image
                  </span>

                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleImageUpload}
                    className="hidden"
                  />

                </label>

              )}

            </div>

          </div>


          {/* Product panel */}
          <aside className="h-fit rounded-2xl border bg-white p-6 shadow-sm">

            <h3 className="text-lg font-bold">
              2. Selected product
            </h3>


            {/* Product image */}
            <div className="mt-5 flex h-40 items-center justify-center overflow-hidden rounded-xl bg-slate-100">

              {product.image ? (

                <img
                  src={product.image}
                  alt={product.name}
                  className="h-full w-full object-contain"
                />

              ) : (

                <span className="text-6xl">
                  🛋️
                </span>

              )}

            </div>


            {/* Product details */}
            <span className="mt-5 inline-block text-xs font-semibold uppercase tracking-wide text-indigo-600">
              {product.category}
            </span>

            <h4 className="mt-2 text-xl font-bold">
              {product.name}
            </h4>

            <p className="mt-2 text-sm text-slate-500">
              {product.material} · {product.color}
            </p>

            <p className="mt-4 text-2xl font-bold">
              ₹{product.price.toLocaleString("en-IN")}
            </p>


            {/* Dimensions */}
            <div className="mt-5 rounded-xl bg-slate-50 p-4">

              <p className="text-sm font-semibold">
                Dimensions
              </p>

              <p className="mt-1 text-sm text-slate-500">
                {product.dimensions.width} ×{" "}
                {product.dimensions.depth} ×{" "}
                {product.dimensions.height} cm
              </p>

            </div>


            {/* Analyze button */}
            <button
              onClick={handleAnalyze}
              disabled={!imageFile || analyzing}
              className="mt-6 w-full rounded-xl bg-indigo-600 px-5 py-3 font-semibold text-white transition hover:bg-indigo-700 disabled:cursor-not-allowed disabled:bg-slate-300"
            >

              {analyzing
                ? "Analyzing your space..."
                : "Analyze My Space"}

            </button>


            {/* Error */}
            {error && (

              <div className="mt-4 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">

                {error}

              </div>

            )}


            {/* Analysis result */}
            {analysis && (

              <div className="mt-6 rounded-2xl border bg-slate-50 p-5">

                <div className="flex items-center justify-between">

                  <h4 className="font-bold">
                    AI Space Analysis
                  </h4>

                  <span className="rounded-full bg-green-100 px-3 py-1 text-sm font-bold text-green-700">
                    {analysis.fit_score}% Fit
                  </span>

                </div>


                {/* Scores */}
                <div className="mt-5 grid grid-cols-2 gap-3">

                  <div className="rounded-xl bg-white p-3">

                    <p className="text-xs text-slate-500">
                      Style Match
                    </p>

                    <p className="mt-1 text-xl font-bold">
                      {analysis.style_match}%
                    </p>

                  </div>


                  <div className="rounded-xl bg-white p-3">

                    <p className="text-xs text-slate-500">
                      Space Used
                    </p>

                    <p className="mt-1 text-xl font-bold">
                      {analysis.space_utilization}%
                    </p>

                  </div>

                </div>


                {/* Recommendation */}
                <div className="mt-4 rounded-xl bg-white p-4">

                  <p className="text-xs font-semibold uppercase tracking-wide text-indigo-600">
                    Recommendation
                  </p>

                  <p className="mt-2 text-sm leading-6 text-slate-600">
                    {analysis.recommendation}
                  </p>

                </div>

              </div>

            )}

          </aside>

        </div>


        {/* AI Visualization */}
        {visualization && (

          <div className="mt-8 rounded-2xl border bg-white p-6 shadow-sm">

            <h3 className="mb-3 text-lg font-bold">
              AI Visualization
            </h3>

            <p className="mb-4 text-sm text-slate-500">
              Preview of your selected furniture placed in the uploaded room.
            </p>

            <div className="overflow-hidden rounded-2xl border bg-slate-100">

              <img
                src={visualization}
                alt="AI visualization with selected furniture"
                className="w-full object-contain"
              />

            </div>

          </div>

        )}

      </section>

    </main>
  );
}
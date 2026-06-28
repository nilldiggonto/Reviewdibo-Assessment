"use client";

import { useEffect, useState, useCallback } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { getProduct } from "@/lib/api";
import { ProductDetail } from "@/lib/types";
import StarRating from "@/components/StarRating";
import ReviewCard from "@/components/ReviewCard";
import ReviewForm from "@/components/ReviewForm";

export default function ProductDetailPage() {
  const params = useParams();
  const productId = Number(params.id);

  const [product, setProduct] = useState<ProductDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchProduct = useCallback(() => {
    setLoading(true);
    getProduct(productId)
      .then(setProduct)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [productId]);

  useEffect(() => {
    fetchProduct();
  }, [fetchProduct]);

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 py-12 animate-pulse">
        <div className="h-6 bg-gray-200 rounded w-24 mb-8" />
        <div className="aspect-video bg-gray-200 rounded-xl mb-8" />
        <div className="h-8 bg-gray-200 rounded w-1/2 mb-4" />
        <div className="h-4 bg-gray-200 rounded w-3/4 mb-8" />
        <div className="space-y-4">
          <div className="h-24 bg-gray-200 rounded" />
          <div className="h-24 bg-gray-200 rounded" />
        </div>
      </div>
    );
  }

  if (error || !product) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 py-12">
        <Link href="/" className="text-blue-600 hover:text-blue-700 text-sm mb-6 inline-block">
          &larr; Back to Products
        </Link>
        <div className="bg-red-50 border border-red-200 text-red-700 p-6 rounded-lg text-center">
          <p className="font-medium">Product not found</p>
          <p className="text-sm mt-1">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 py-12">
      <Link href="/" className="text-blue-600 hover:text-blue-700 text-sm mb-6 inline-block">
        &larr; Back to Products
      </Link>

      {product.image_url && (
        <div className="aspect-video bg-gray-100 rounded-xl overflow-hidden mb-8">
          <img
            src={product.image_url}
            alt={product.title}
            className="w-full h-full object-cover"
          />
        </div>
      )}

      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-3">{product.title}</h1>
        <p className="text-gray-600 leading-relaxed mb-4">{product.description}</p>
        <div className="flex items-center gap-3">
          <StarRating rating={product.average_rating ?? 0} size="md" />
          <span className="text-lg font-semibold text-gray-800">
            {product.average_rating?.toFixed(1) ?? "N/A"}
          </span>
          <span className="text-gray-400">
            ({product.review_count} {product.review_count === 1 ? "review" : "reviews"})
          </span>
        </div>
      </div>

      <div className="mb-8">
        <ReviewForm productId={productId} onReviewSubmitted={fetchProduct} />
      </div>

      <div>
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          Reviews ({product.review_count})
        </h2>
        {product.reviews.length > 0 ? (
          <div className="space-y-4">
            {product.reviews.map((review) => (
              <ReviewCard key={review.id} review={review} />
            ))}
          </div>
        ) : (
          <p className="text-gray-400 text-center py-8">
            No reviews yet. Be the first to review this product!
          </p>
        )}
      </div>
    </div>
  );
}
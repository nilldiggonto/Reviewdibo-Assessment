"use client";

interface StarRatingProps {
  rating: number;
  maxRating?: number;
  size?: "sm" | "md" | "lg";
  interactive?: boolean;
  onRate?: (rating: number) => void;
}

export default function StarRating({
  rating,
  maxRating = 5,
  size = "md",
  interactive = false,
  onRate,
}: StarRatingProps) {
  const sizeClass = { sm: "text-sm", md: "text-xl", lg: "text-2xl" }[size];

  return (
    <div className={`flex items-center gap-0.5 ${sizeClass}`}>
      {Array.from({ length: maxRating }, (_, i) => {
        const starValue = i + 1;
        const filled = starValue <= Math.round(rating);
        return (
          <span
            key={i}
            className={`${interactive ? "cursor-pointer hover:scale-110 transition-transform" : ""} ${
              filled ? "text-yellow-400" : "text-gray-300"
            }`}
            onClick={() => interactive && onRate?.(starValue)}
            role={interactive ? "button" : undefined}
            aria-label={interactive ? `Rate ${starValue} stars` : undefined}
          >
            ★
          </span>
        );
      })}
    </div>
  );
}
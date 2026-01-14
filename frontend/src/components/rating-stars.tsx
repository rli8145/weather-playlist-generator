import { useState } from "react";
import { Star } from "lucide-react";
import { cn } from "@/lib/utils";

interface RatingStarsProps {
  onRate: (rating: number) => void;
  initialRating?: number;
}

const RatingStars = ({ onRate, initialRating = 0 }: RatingStarsProps) => {
  const [rating, setRating] = useState(initialRating);
  const [hoverRating, setHoverRating] = useState(0);
  const [hasRated, setHasRated] = useState(false);

  const handleRate = (value: number) => {
    setRating(value);
    setHasRated(true);
    onRate(value);
  };

  return (
    <div className="glass-card rounded-xl p-6 max-w-md w-full animate-fade-in animation-delay-200">
      <h3 className="text-lg font-semibold text-foreground mb-2 text-center">
        {hasRated ? "Thanks for rating!" : "How's this playlist?"}
      </h3>
      <p className="text-sm text-muted-foreground text-center mb-4">
        {hasRated
          ? "We'll use this to improve recommendations"
          : "Help us curate better playlists for you"}
      </p>

      <div className="flex justify-center gap-2">
        {[1, 2, 3, 4, 5].map((star) => (
          <button
            key={star}
            onClick={() => handleRate(star)}
            onMouseEnter={() => setHoverRating(star)}
            onMouseLeave={() => setHoverRating(0)}
            className="p-1 transition-transform hover:scale-110 active:scale-95"
          >
            <Star
              className={cn(
                "w-8 h-8 transition-colors",
                (hoverRating || rating) >= star
                  ? "fill-accent text-accent"
                  : "text-muted-foreground/40"
              )}
            />
          </button>
        ))}
      </div>

      {hasRated && (
        <p className="text-center text-accent text-sm mt-4 animate-fade-in">
          You rated this {rating} out of 5 stars
        </p>
      )}
    </div>
  );
};

export default RatingStars;

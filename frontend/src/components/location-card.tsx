import { MapPin, Loader2, AlertCircle, RefreshCw } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

interface LocationPermissionCardProps {
  isLoading: boolean;
  error: string | null;
  onRequestLocation: () => void;
  onSkip: () => void;
}

const LocationPermissionCard = ({
  isLoading,
  error,
  onRequestLocation,
  onSkip,
}: LocationPermissionCardProps) => {
  if (isLoading) {
    return (
      <Card className="bg-secondary/50 backdrop-blur-sm border-accent/20 animate-fade-in">
        <CardContent className="flex flex-col items-center gap-4 py-6">
          <Loader2 className="w-8 h-8 text-accent animate-spin" />
          <p className="text-sm text-muted-foreground">Detecting your location...</p>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className="bg-secondary/50 backdrop-blur-sm border-destructive/20 animate-fade-in">
        <CardContent className="flex flex-col items-center gap-4 py-6">
          <AlertCircle className="w-8 h-8 text-destructive" />
          <p className="text-sm text-destructive">{error}</p>
          <div className="flex gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={onRequestLocation}
              className="gap-2"
            >
              <RefreshCw className="w-4 h-4" />
              Try Again
            </Button>
            <Button variant="ghost" size="sm" onClick={onSkip}>
              Use Default
            </Button>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="bg-secondary/50 backdrop-blur-sm border-accent/20 animate-fade-in">
      <CardContent className="flex flex-col items-center gap-4 py-6">
        <div className="p-3 rounded-full bg-accent/20">
          <MapPin className="w-6 h-6 text-accent" />
        </div>
        <div className="text-center">
          <h3 className="font-semibold text-foreground mb-1">
            Allow Location Access
          </h3>
          <p className="text-sm text-muted-foreground max-w-xs">
            Get personalized weather playlists based on your current location and conditions
          </p>
        </div>
        <div className="flex gap-2">
          <Button onClick={onRequestLocation} className="gap-2">
            <MapPin className="w-4 h-4" />
            Allow Location
          </Button>
          <Button variant="ghost" onClick={onSkip}>
            Skip
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};

export default LocationPermissionCard;

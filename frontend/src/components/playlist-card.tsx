import { Music, ExternalLink, Clock } from "lucide-react";

interface Track {
  id: number;
  title: string;
  artist: string;
  duration: string;
}

interface PlaylistCardProps {
  name: string;
  description: string;
  trackCount: number;
  coverImage: string;
  tracks: Track[];
}

const PlaylistCard = ({ name, description, trackCount, coverImage, tracks }: PlaylistCardProps) => {
  return (
    <div className="glass-card rounded-2xl p-6 max-w-md w-full animate-fade-in">
      {/* Header */}
      <div className="flex gap-4 mb-6">
        <div className="relative group">
          <img
            src={coverImage}
            alt={name}
            className="w-28 h-28 rounded-xl object-cover shadow-2xl shadow-accent/20 transition-transform group-hover:scale-105"
          />
          <div className="absolute inset-0 bg-black/20 rounded-xl opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
            <Music className="w-8 h-8 text-white" />
          </div>
        </div>
        
        <div className="flex flex-col justify-center">
          <span className="text-xs uppercase tracking-wider text-muted-foreground mb-1">
            Playlist
          </span>
          <h2 className="text-xl font-bold text-foreground mb-1">{name}</h2>
          <p className="text-sm text-muted-foreground">{description}</p>
          <span className="text-xs text-muted-foreground mt-2">
            {trackCount} songs
          </span>
        </div>
      </div>

      {/* Track List */}
      <div className="space-y-2 mb-6">
        {tracks.slice(0, 5).map((track, index) => (
          <div
            key={track.id}
            className="flex items-center gap-3 p-2 rounded-lg hover:bg-white/5 transition-colors group cursor-pointer"
          >
            <span className="w-5 text-xs text-muted-foreground text-center group-hover:text-accent">
              {index + 1}
            </span>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-foreground truncate">{track.title}</p>
              <p className="text-xs text-muted-foreground truncate">{track.artist}</p>
            </div>
            <div className="flex items-center gap-2 text-muted-foreground">
              <Clock className="w-3 h-3" />
              <span className="text-xs">{track.duration}</span>
            </div>
          </div>
        ))}
      </div>

      {/* Open in Spotify Button */}
      <button className="w-full bg-spotify hover:bg-spotify-hover text-white font-semibold py-3 px-6 rounded-full flex items-center justify-center gap-2 transition-all hover:scale-[1.02] active:scale-[0.98]">
        <ExternalLink className="w-4 h-4" />
        Open in Spotify
      </button>
    </div>
  );
};

export default PlaylistCard;

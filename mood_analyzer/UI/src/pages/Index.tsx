import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Loader2 } from "lucide-react";

const moods = [
  { value: "happy", label: "😊 Happy" },
  { value: "sad", label: "😢 Sad" },
  { value: "anxious", label: "😰 Anxious" },
  { value: "calm", label: "😌 Calm" },
  { value: "excited", label: "🎉 Excited" },
  { value: "frustrated", label: "😤 Frustrated" },
  { value: "grateful", label: "🙏 Grateful" },
  { value: "tired", label: "😴 Tired" },
];

const Index = () => {
  const [selectedMood, setSelectedMood] = useState<string>("");
  const [description, setDescription] = useState("");
  
  const [response, setResponse] = useState("");

  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async () => {
    if (!selectedMood) return;

    setIsLoading(true);
    setResponse("");

    try {
      // Replace this URL with your actual API endpoint
        
      const apiResponse = await fetch(
        `http://127.0.0.1:8082/wellnessadvice?mood_type=${encodeURIComponent(selectedMood)}&mood_description=${encodeURIComponent(description)}`,
        {
          method: "GET",
        }
      );

      // const apiResponse = await fetch("http://localhost:8082/wellnessadvice", {
      //   method: "POST",
      //   headers: {
      //     "Content-Type": "application/json",
      //   },
      //   body: JSON.stringify({
      //     mood_type: selectedMood,
      //     mood_description: description,
      //   }),
      // });

      // const data = await apiResponse.json();
      const data = await apiResponse.text();
      setResponse(data);
    } catch (error) {
      setResponse("Error: Unable to reach the API. Please check the endpoint.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-secondary/20 to-background flex items-center justify-center p-4">
      <Card className="w-full max-w-md shadow-xl border-border/50">
        <CardHeader className="text-center">
          <CardTitle className="text-2xl font-semibold text-foreground">
            How are you feeling?
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="space-y-2">
            <Label htmlFor="mood-select" className="text-sm font-medium">
              Select your mood
            </Label>
            <Select value={selectedMood} onValueChange={setSelectedMood}>
              <SelectTrigger id="mood-select" className="w-full">
                <SelectValue placeholder="Choose a mood..." />
              </SelectTrigger>
              <SelectContent className="bg-popover">
                {moods.map((mood) => (
                  <SelectItem key={mood.value} value={mood.value}>
                    {mood.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label htmlFor="description" className="text-sm font-medium">
              Describe your mood in detail
            </Label>
            <Textarea
              id="description"
              placeholder="Tell us more about how you're feeling..."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="min-h-[120px] resize-none"
            />
          </div>

          <Button
            onClick={handleSubmit}
            disabled={!selectedMood || isLoading}
            className="w-full"
          >
            {isLoading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Processing...
              </>
            ) : (
              "Submit"
            )}
          </Button>

          {response && (
            <div className="space-y-2">
              <Label className="text-sm font-medium">API Response</Label>
              <div className="p-4 rounded-lg bg-muted/50 border border-border text-sm text-foreground whitespace-pre-wrap">
                {response}
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default Index;

public class EmotionChoice
{
    public int Id { get; set; }
    public string UserName { get; set; }
    public string Emotion { get; set; }
    public int Intensity { get; set; }
    public string TriggerFactor { get; set; }

    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
}
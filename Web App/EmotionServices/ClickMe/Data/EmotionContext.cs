using Microsoft.EntityFrameworkCore;
using ClickMe.Models;  // Make sure namespace matches your Models folder

namespace ClickMe.Data
{
    public class EmotionContext : DbContext
    {
        public EmotionContext(DbContextOptions<EmotionContext> options) : base(options) { }

        public DbSet<EmotionChoice> EmotionChoices { get; set; }
    }
}
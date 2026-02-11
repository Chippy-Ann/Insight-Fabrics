using Microsoft.AspNetCore.Mvc;
using ClickMe.Data; // update namespace
using ClickMe.Models;

public class EmotionController : Controller
{
    private readonly EmotionContext _context;

    public EmotionController(EmotionContext context)
    {
        _context = context;
    }

    [HttpGet]
    public IActionResult Index()
    {
        return View();
    }

    [HttpPost]
    public IActionResult Submit(string userName, string emotion,string triggerfactor, int intensity)
    {
        if (!string.IsNullOrEmpty(userName) && !string.IsNullOrEmpty(emotion))
        {
            _context.EmotionChoices.Add(new EmotionChoice
            {
                UserName = userName,
                Emotion = emotion,
                TriggerFactor = triggerfactor,
                Intensity= intensity

            });
            _context.SaveChanges();
        }
        return RedirectToAction("Thanks");
    }

    public IActionResult Thanks()
    {
        return View();
    }
}
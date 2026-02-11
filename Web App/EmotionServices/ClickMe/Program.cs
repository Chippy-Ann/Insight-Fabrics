using ClickMe.Data;
using Microsoft.EntityFrameworkCore;
using Azure.Identity;

var builder = WebApplication.CreateBuilder(args);



// Add Key Vault
// var keyVaultName = builder.Configuration["KeyVault:Name"];
// var kvUri = $"https://{keyVaultName}.vault.azure.net/";
// builder.Configuration.AddAzureKeyVault(new Uri(kvUri), new DefaultAzureCredential());


// Configure DbContext using connection string from Key Vault
builder.Services.AddDbContext<EmotionContext>(options =>
    options.UseSqlServer(builder.Configuration["DefaultConnection"])
  //options.UseSqlServer("Server=tcp:sqlserverazdatapltfrm.database.windows.net,1433;Database=sqlemotiondb;User ID=sqladminuser;Password=Chippy@123!;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;")
);


// Add services to the container.
builder.Services.AddControllersWithViews().AddRazorRuntimeCompilation();;

var app = builder.Build();

// Configure the HTTP request pipeline.
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Home/Error");
    // The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
    app.UseHsts();
}
app.UseHttpsRedirection();
app.UseStaticFiles();
app.UseRouting();

app.UseAuthorization();

app.MapStaticAssets();

app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Emotion}/{action=Index}/{id?}")
    .WithStaticAssets();


app.Run();

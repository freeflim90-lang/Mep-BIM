using Autodesk.Revit.UI;

namespace RevitLUAChat
{
    public class App : IExternalApplication
    {
        public Result OnStartup(UIControlledApplication app)
        {
            var panel = app.CreateRibbonPanel("LUA BIM LABS");
            var buttonData = new PushButtonData(
                "LUAChat",
                "LUA BIM\nChat",
                typeof(App).Assembly.Location,
                "RevitLUAChat.ChatCommand");

            buttonData.ToolTip = "LUA BIM LABS Revit Assistant 채팅 창을 엽니다.";
            panel.AddItem(buttonData);

            return Result.Succeeded;
        }

        public Result OnShutdown(UIControlledApplication app)
        {
            return Result.Succeeded;
        }
    }
}

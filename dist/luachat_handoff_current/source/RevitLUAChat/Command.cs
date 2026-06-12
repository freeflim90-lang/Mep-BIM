using System;
using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;

namespace RevitLUAChat
{
    [Transaction(TransactionMode.Manual)]
    public class ChatCommand : IExternalCommand
    {
        public Result Execute(ExternalCommandData commandData, ref string message, ElementSet elements)
        {
            try
            {
                var userId = commandData.Application.Application.Username;
                if (string.IsNullOrEmpty(userId)) userId = "revit_user";
                var window = new ChatWindow(commandData.Application, userId);
                window.Show();
                return Result.Succeeded;
            }
            catch (Exception ex)
            {
                message = ex.Message;
                return Result.Failed;
            }
        }
    }
}

using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Media;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;
using MediaColor = System.Windows.Media.Color;
using WpfVisibility = System.Windows.Visibility;
namespace RevitLUAChat
{
    public partial class ChatWindow : Window
    {
        private const string WelcomeMessage = "안녕하세요. LUA BIM LABS Revit Assistant입니다. Revit, Dynamo, 설비 BIM 질문을 조직 지식 기준으로 도와드릴게요.";
        private readonly UIApplication _uiApp;
        private readonly string _userId;
        private string _lastUserMessage = string.Empty;

        public ChatWindow(UIApplication uiApp, string userId)
        {
            InitializeComponent();
            _uiApp = uiApp;
            _userId = userId;

            UpdateRevitContext();
            AddBotMessage(WelcomeMessage);
        }

        private void UpdateRevitContext()
        {
            try
            {
                var document = _uiApp.ActiveUIDocument?.Document;
                var selection = _uiApp.ActiveUIDocument?.Selection?.GetElementIds();

                if (document == null || selection == null || selection.Count == 0)
                {
                    ContextLabel.Text = "선택된 Revit 요소가 없습니다.";
                    return;
                }

                var element = document.GetElement(selection.First());
                ContextLabel.Text = element != null
                    ? $"선택 요소: {element.Name} ({element.Category?.Name ?? "카테고리 없음"})"
                    : "선택된 Revit 요소 정보를 읽을 수 없습니다.";
            }
            catch
            {
                ContextLabel.Text = "Revit 선택 정보를 불러오는 중 문제가 발생했습니다.";
            }
        }

        private string GetRevitContext()
        {
            try
            {
                var document = _uiApp.ActiveUIDocument?.Document;
                var selection = _uiApp.ActiveUIDocument?.Selection?.GetElementIds();
                if (document == null || selection == null || selection.Count == 0)
                {
                    return string.Empty;
                }

                var builder = new StringBuilder();
                foreach (var id in selection)
                {
                    var element = document.GetElement(id);
                    if (element == null)
                    {
                        continue;
                    }

                    builder.AppendLine($"요소명: {element.Name}");
                    builder.AppendLine($"카테고리: {element.Category?.Name ?? "없음"}");
#if NET48
#pragma warning disable CS0618
                    builder.AppendLine($"ID: {element.Id.IntegerValue}");
#pragma warning restore CS0618
#else
                    builder.AppendLine($"ID: {element.Id.Value}");
#endif
                    builder.AppendLine();
                }

                return builder.ToString().Trim();
            }
            catch
            {
                return string.Empty;
            }
        }

        private void AddUserMessage(string text)
        {
            var bubble = CreateMessageBubble(
                text,
                MediaColor.FromRgb(0x89, 0xB4, 0xFA),
                MediaColor.FromRgb(0x1E, 0x1E, 0x2E),
                new Thickness(50, 4, 0, 4),
                HorizontalAlignment.Right,
                new CornerRadius(12, 12, 2, 12));

            ChatPanel.Children.Add(bubble);
            ChatScroll.ScrollToEnd();
        }

        private void AddBotMessage(string text)
        {
            var bubble = CreateMessageBubble(
                text,
                MediaColor.FromRgb(0x31, 0x32, 0x44),
                MediaColor.FromRgb(0xCD, 0xD6, 0xF4),
                new Thickness(0, 4, 50, 4),
                HorizontalAlignment.Left,
                new CornerRadius(12, 12, 12, 2));

            ChatPanel.Children.Add(bubble);

            if (text != WelcomeMessage)
            {
                AddFeedbackButtons(text);
            }

            ChatScroll.ScrollToEnd();
        }

        private Border CreateMessageBubble(
            string text,
            MediaColor backgroundColor,
            MediaColor foregroundColor,
            Thickness margin,
            HorizontalAlignment alignment,
            CornerRadius cornerRadius)
        {
            var border = new Border
            {
                Background = new SolidColorBrush(backgroundColor),
                CornerRadius = cornerRadius,
                Padding = new Thickness(10, 6, 10, 6),
                Margin = margin,
                HorizontalAlignment = alignment
            };

            border.Child = new TextBlock
            {
                Text = text,
                TextWrapping = TextWrapping.Wrap,
                Foreground = new SolidColorBrush(foregroundColor),
                FontSize = 13
            };

            return border;
        }

        private void AddFeedbackButtons(string botMessage)
        {
            var panel = new StackPanel
            {
                Orientation = Orientation.Horizontal,
                Margin = new Thickness(0, 2, 0, 6)
            };

            var goodButton = CreateFeedbackButton("좋아요");
            var badButton = CreateFeedbackButton("아쉬워요");

            goodButton.Click += async (_, _) =>
            {
                await ApiClient.SendFeedback(_userId, true, _lastUserMessage, botMessage);
                goodButton.Content = "저장됨";
                badButton.IsEnabled = false;
            };

            badButton.Click += async (_, _) =>
            {
                await ApiClient.SendFeedback(_userId, false, _lastUserMessage, botMessage);
                badButton.Content = "저장됨";
                goodButton.IsEnabled = false;
            };

            panel.Children.Add(goodButton);
            panel.Children.Add(badButton);
            ChatPanel.Children.Add(panel);
        }

        private Button CreateFeedbackButton(string label)
        {
            return new Button
            {
                Content = label,
                Height = 24,
                Margin = new Thickness(0, 0, 6, 0),
                Padding = new Thickness(8, 0, 8, 0),
                Background = Brushes.Transparent,
                BorderBrush = new SolidColorBrush(MediaColor.FromRgb(0x6C, 0x70, 0x86)),
                BorderThickness = new Thickness(1),
                Foreground = Brushes.White,
                FontSize = 11,
                Cursor = Cursors.Hand
            };
        }

        private void AddLoadingMessage()
        {
            ChatPanel.Children.Add(new TextBlock
            {
                Text = "응답을 생성하는 중입니다...",
                Foreground = new SolidColorBrush(MediaColor.FromRgb(0x6C, 0x70, 0x86)),
                Margin = new Thickness(0, 4, 0, 4),
                FontSize = 12,
                Name = "LoadingMessage"
            });

            ChatScroll.ScrollToEnd();
        }

        private void RemoveLoadingMessage()
        {
            for (int i = ChatPanel.Children.Count - 1; i >= 0; i--)
            {
                if (ChatPanel.Children[i] is TextBlock textBlock && textBlock.Name == "LoadingMessage")
                {
                    ChatPanel.Children.RemoveAt(i);
                    break;
                }
            }
        }

        private void InputBox_GotFocus(object sender, RoutedEventArgs e)
        {
            PlaceholderText.Visibility = WpfVisibility.Collapsed;
        }

        private void InputBox_LostFocus(object sender, RoutedEventArgs e)
        {
            if (string.IsNullOrWhiteSpace(InputBox.Text))
            {
                PlaceholderText.Visibility = WpfVisibility.Visible;
            }
        }

        private async void SendBtn_Click(object sender, RoutedEventArgs e)
        {
            await SendAsync();
        }

        private async void InputBox_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.Key == Key.Return)
            {
                e.Handled = true;
                await SendAsync();
            }
        }

        private async Task SendAsync()
        {
            var text = InputBox.Text.Trim();
            if (string.IsNullOrWhiteSpace(text))
            {
                return;
            }

            InputBox.Text = string.Empty;
            PlaceholderText.Visibility = WpfVisibility.Visible;
            SendBtn.IsEnabled = false;

            _lastUserMessage = text;
            AddUserMessage(text);
            AddLoadingMessage();
            UpdateRevitContext();

            try
            {
                var context = GetRevitContext();
                var response = await ApiClient.SendMessage(_userId, text, context);
                RemoveLoadingMessage();
                AddBotMessage(response);
            }
            finally
            {
                SendBtn.IsEnabled = true;
            }
        }
    }
}

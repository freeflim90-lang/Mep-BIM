using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;

namespace BIMCommandCenter.Services
{
    public class LuaChatRequest
    {
        [JsonProperty("user_id")] public string UserId { get; set; } = "revit_user";
        [JsonProperty("message")] public string Message { get; set; } = string.Empty;
        [JsonProperty("revit_context")] public string RevitContext { get; set; } = string.Empty;
        [JsonProperty("client_version")] public string ClientVersion { get; set; } = "LUAChat";
        [JsonProperty("source")] public string Source { get; set; } = "revit-addin";
    }

    public class LuaChatSource
    {
        [JsonProperty("path")] public string Path { get; set; } = string.Empty;
        [JsonProperty("score")] public int Score { get; set; }
    }

    public class LuaChatResponse
    {
        [JsonProperty("status")] public string Status { get; set; } = string.Empty;
        [JsonProperty("brand")] public string Brand { get; set; } = string.Empty;
        [JsonProperty("agent")] public string Agent { get; set; } = string.Empty;
        [JsonProperty("answer")] public string Answer { get; set; } = string.Empty;
        [JsonProperty("note_path")] public string NotePath { get; set; } = string.Empty;
        [JsonProperty("needs_more")] public bool NeedsMore { get; set; }
        [JsonProperty("sources")] public List<LuaChatSource> Sources { get; set; } = new List<LuaChatSource>();
        [JsonProperty("reason")] public string Reason { get; set; } = string.Empty;
    }

    public class LuaChatFeedbackRequest
    {
        [JsonProperty("user_id")] public string UserId { get; set; } = "revit_user";
        [JsonProperty("message")] public string Message { get; set; } = string.Empty;
        [JsonProperty("answer")] public string Answer { get; set; } = string.Empty;
        [JsonProperty("is_good")] public bool IsGood { get; set; }
        [JsonProperty("note_path")] public string NotePath { get; set; } = string.Empty;
        [JsonProperty("feedback")] public string Feedback { get; set; } = string.Empty;
    }

    public static class LuaChatApiClient
    {
        private static readonly HttpClient Http = new HttpClient();

        private const string DefaultChatUrl = "http://127.0.0.1:8000/api/luachat";
        private static readonly string ChatUrl =
            (Environment.GetEnvironmentVariable("LUA_CHAT_URL") ?? DefaultChatUrl).TrimEnd('/');

        private static readonly string Token =
            Environment.GetEnvironmentVariable("LUA_CHAT_TOKEN") ?? string.Empty;

        public static string LastNotePath { get; private set; } = string.Empty;
        public static string LastAnswer { get; private set; } = string.Empty;

        public static async Task<LuaChatResponse> SendMessage(
            string userId,
            string message,
            string revitContext)
        {
            var request = new LuaChatRequest
            {
                UserId = string.IsNullOrWhiteSpace(userId) ? "revit_user" : userId,
                Message = message ?? string.Empty,
                RevitContext = revitContext ?? string.Empty
            };

            var response = await PostJson<LuaChatResponse>(ChatUrl, request);
            LastNotePath = response.NotePath ?? string.Empty;
            LastAnswer = response.Answer ?? string.Empty;
            return response;
        }

        public static async Task<bool> SendFeedback(
            string userId,
            string message,
            string answer,
            bool isGood,
            string feedback)
        {
            var request = new LuaChatFeedbackRequest
            {
                UserId = string.IsNullOrWhiteSpace(userId) ? "revit_user" : userId,
                Message = message ?? string.Empty,
                Answer = answer ?? LastAnswer ?? string.Empty,
                IsGood = isGood,
                NotePath = LastNotePath ?? string.Empty,
                Feedback = feedback ?? string.Empty
            };

            var feedbackUrl = ChatUrl.EndsWith("/api/luachat", StringComparison.OrdinalIgnoreCase)
                ? ChatUrl + "/feedback"
                : ChatUrl.TrimEnd('/') + "/feedback";

            var response = await PostJson<LuaChatResponse>(feedbackUrl, request);
            return response.Status == "updated" || response.Status == "ok";
        }

        private static async Task<T> PostJson<T>(string url, object body) where T : LuaChatResponse, new()
        {
            var json = JsonConvert.SerializeObject(body);
            using (var request = new HttpRequestMessage(HttpMethod.Post, url))
            {
                request.Content = new StringContent(json, Encoding.UTF8, "application/json");
                if (!string.IsNullOrWhiteSpace(Token))
                {
                    request.Headers.Authorization = new AuthenticationHeaderValue("Bearer", Token);
                }

                using (var response = await Http.SendAsync(request))
                {
                    var text = await response.Content.ReadAsStringAsync();
                    if (!response.IsSuccessStatusCode)
                    {
                        return new T
                        {
                            Status = "error",
                            Reason = $"HTTP {(int)response.StatusCode}: {text}"
                        };
                    }

                    return JsonConvert.DeserializeObject<T>(text) ?? new T
                    {
                        Status = "error",
                        Reason = "Empty response"
                    };
                }
            }
        }
    }
}

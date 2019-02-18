using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.WebSockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using UnityEngine;

[System.Serializable]
public class MachineState {
    public LimitWarnings limitWarnings;
    public ZeroLevel zeroLevel;
    public Angles angles;

    public static MachineState CreateFromJSON(string jsonString)
    {
        return JsonUtility.FromJson<MachineState>(jsonString);
    }
}

[System.Serializable]
public class LimitWarnings {
    public Boolean left = false;
    public Boolean right = false;
    public Boolean upper = false;
    public Boolean lower = false;
    public Boolean forward = false;
    public Boolean property = false;
    public Boolean overload = false;

    public static LimitWarnings CreateFromJSON(string jsonString)
    {
        return JsonUtility.FromJson<LimitWarnings>(jsonString);
    }
}

[System.Serializable]
public class ZeroLevel {
    public float height_from_zero = 0.0f;
    public float distance_to_zero = 0.0f;
    public float height_to_slope_from_zero = 0.0f;

    public static ZeroLevel CreateFromJSON(string jsonString)
    {
        return JsonUtility.FromJson<ZeroLevel>(jsonString);
    }
}

[System.Serializable]
public class Angles {
    public int main_boom = 0;
    public int digging_arm = 0;
    public int bucket = 0;
    public int heading = 0;
    public int frame_pitch = 0;
    public int frame_roll = 0;

    public static Angles CreateFromJSON(string jsonString)
    {
        return JsonUtility.FromJson<Angles>(jsonString);
    }
}

public class Network : MonoBehaviour
{
    static ClientWebSocket webSocket = null;
    private const int sendChunkSize = 256;
    private const int receiveChunkSize = 64;
    private const bool verbose = true;
    private static readonly TimeSpan delay = TimeSpan.FromMilliseconds(1000);
    public static MachineState state = MachineState.CreateFromJSON("");
    private static string address;

    void Start()
    {
        Debug.Log("Init network");
    }

    // Update is called once per frame
    async void Update()
    {
        /*
        if (webSocket.State == WebSocketState.Closed) {
            ConsoleHandler.Instance.AddItemToConsole(new ListItem("Reconnecting...",1));
            await Connect("ws://" + address + ":9000");
        }
        Debug.Log(state);
        */
        
    }

    void OnDestroy()
    {
        if (webSocket != null) {
            webSocket.Abort();
            webSocket.Dispose();
        }
        Debug.Log("");
        Debug.Log("WebSocket disposed.");
    }

    public static async Task ConnectToServer(string ip) {
        address = ip;
        ConsoleHandler.Instance.AddItemToConsole(new ListItem("Connecting...",1));
        await Connect("ws://" + address + ":9000");
    }

    public static async Task Connect(string uri)
    {
        try
        {
            webSocket = new ClientWebSocket();
            await webSocket.ConnectAsync(new Uri(uri), CancellationToken.None);
            await Task.WhenAll(ReadRotation(webSocket));
        }
        catch (Exception ex)
        {
            Debug.Log($"Exception: {ex.Message}");
        }
        finally
        {
            if (webSocket != null)
                webSocket.Dispose();
            Debug.Log("");
            Debug.Log("WebSocket closed.");
        }
    }

    private static async Task Echo(ClientWebSocket webSocket)
    {
        while (webSocket.State == WebSocketState.Open)
        {                
            var result = await ReceiveStringAsync();
            LogStatus(true, result);
            await SendStringAsync("ping");
            LogStatus(false, "ping");
            await Task.Delay(delay);
        }
        if(webSocket.State == WebSocketState.Closed) {
            Debug.Log("WebSocket closed.");
        }
    }

    private static async Task ReadRotation(ClientWebSocket webSocket)
    {
        while (webSocket.State == WebSocketState.Open)
        {
            var result = await ReceiveStringAsync();
            Debug.Log(result);
            var tempstate = JsonUtility.FromJson<MachineState>(result);
            state = tempstate;
        }
        if(webSocket.State == WebSocketState.Closed) {
            Debug.Log("WebSocket closed.");
        }
    }

    private static Task SendStringAsync(string data, CancellationToken ct = default(CancellationToken))
    {
        var buffer = Encoding.UTF8.GetBytes(data);
        var segment = new ArraySegment<byte>(buffer);
        return webSocket.SendAsync(segment, WebSocketMessageType.Text, true, ct);
    }

    private static async Task<string> ReceiveStringAsync(CancellationToken ct = default(CancellationToken))
    {
        var buffer = new ArraySegment<byte>(new byte[8192]);
        using (var ms = new MemoryStream())
        {
            WebSocketReceiveResult result;
            do
            {
                ct.ThrowIfCancellationRequested();

                result = await webSocket.ReceiveAsync(buffer, ct);
                ms.Write(buffer.Array, buffer.Offset, result.Count);
            }
            while (!result.EndOfMessage);

            ms.Seek(0, SeekOrigin.Begin);
            if (result.MessageType != WebSocketMessageType.Text)
            {
                return null;
            }

            // Encoding UTF8: https://tools.ietf.org/html/rfc6455#section-5.6
            using (var reader = new StreamReader(ms, Encoding.UTF8))
            {
                return await reader.ReadToEndAsync();
            }
        }
    }

    private static void LogStatus(bool receiving, string message)
    {
        Debug.Log($"{(receiving ? "Received" : "Sent")} bytes... ");
        Debug.Log(message);
    }
}

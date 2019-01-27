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
public class Rotations {
    public float x = 0.0f;
    public float y = 0.0f;
    public float z = 0.0f;

    public static Rotations CreateFromJSON(string jsonString)
    {
        return JsonUtility.FromJson<Rotations>(jsonString);
    }
}

public class NetworkedCube : MonoBehaviour
{
    static ClientWebSocket webSocket = null;
    private const int sendChunkSize = 256;
    private const int receiveChunkSize = 64;
    private const bool verbose = true;
    private static readonly TimeSpan delay = TimeSpan.FromMilliseconds(1000);
    private static float rotationX = 0.0f;
    private static float rotationY = 0.0f;
    private static float rotationZ = 0.0f;

    async void Start()
    {
        Debug.Log("asd");
        await Connect("ws://localhost:9000");
    }

    // Update is called once per frame
    async void Update()
    {
        if(webSocket.State == WebSocketState.Closed) {
            Debug.Log("Reconnecting....");
            await Connect("ws://localhost:9000");
        }
        transform.eulerAngles = new Vector3(1 * rotationX * 360, 1 * rotationY * 360, 1 * rotationZ * 360);
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
            rotationX = JsonUtility.FromJson<Rotations>(result).x;
            rotationY = JsonUtility.FromJson<Rotations>(result).y;
            rotationZ = JsonUtility.FromJson<Rotations>(result).z;
        }
        if(webSocket.State == WebSocketState.Closed) {
            Debug.Log("WebSocket closed.");
        }
    }

    // private static async Task Send(ClientWebSocket webSocket)
    // {
    //     //var random = new System.Random();
    //     //byte[] buffer = new byte[sendChunkSize];
    //     byte[] buffer = "ping".ToCharArray();

    //     while (webSocket.State == WebSocketState.Open)
    //     {
    //         //random.NextBytes(buffer);

    //         await webSocket.SendAsync(new ArraySegment<byte>(buffer), WebSocketMessageType.Text, false, CancellationToken.None);
    //         LogStatus(false, buffer, buffer.Length);

    //         await Task.Delay(delay);
    //     }
    // }

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

    // private static async Task Receive(ClientWebSocket webSocket)
    // {
    //     byte[] buffer = new byte[receiveChunkSize];
    //     while (webSocket.State == WebSocketState.Open)
    //     {                
    //         var result = await webSocket.ReceiveAsync(new ArraySegment<byte>(buffer), CancellationToken.None);
    //         if (result.MessageType == WebSocketMessageType.Close)
    //         {
    //             await webSocket.CloseAsync(WebSocketCloseStatus.NormalClosure, string.Empty, CancellationToken.None);
    //         }
    //         else
    //         {
    //             LogStatus(true, buffer, result.Count);
    //         }
    //     }
    // }

    private static void LogStatus(bool receiving, string message)
    {
        Debug.Log($"{(receiving ? "Received" : "Sent")} bytes... ");
        Debug.Log(message);
    }
}

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

public class Network : MonoBehaviour
{
    static ClientWebSocket webSocket = new ClientWebSocket();
    private const int sendChunkSize = 256;
    private const int receiveChunkSize = 64;
    private const bool verbose = true;
    private static readonly TimeSpan delay = TimeSpan.FromMilliseconds(1000);
    private static string address;
    private static GameObject stateObject;
    const int maxConnectionAttempts = 5;
    private static int connectionAttempts = 0;

    void Start()
    {
        Debug.Log("Init network");
        stateObject = GameObject.Find("MachineState");
    }

    void Update()
    {

    }

    void OnDestroy()
    {
        if (webSocket != null) {
            webSocket.Abort();
            webSocket.Dispose();
        }
        Debug.Log("WebSocket disposed.");
    }

    public static async Task ConnectToServer(string ip) {
        address = ip;
        ConsoleHandlerR.Instance.AddItemToConsole(new ListItemR("Connecting...",1));
        webSocket = new ClientWebSocket();
        await Connect("ws://" + address + ":9000");
    }

    private static async Task Reconnect() {
        ConsoleHandlerR.Instance.AddItemToConsole(new ListItemR("Lost connection, reconnecting in 5...",1));
        connectionAttempts += 1;
        await Task.Delay(TimeSpan.FromSeconds(5));
        await ConnectToServer(address);
    }

    public static async Task Connect(string uri)
    {
        try
        {
            await webSocket.ConnectAsync(new Uri(uri), CancellationToken.None);
            ConsoleHandlerR.Instance.AddItemToConsole(new ListItemR($"Connected to {address}",1));
            connectionAttempts += 1;
            await Task.WhenAll(ReceiveState(webSocket));
        }
        catch (Exception ex)
        {
            Debug.Log($"Exception: {ex.Message}");
            Debug.Log(webSocket.State);
        }
        finally
        {
            if(webSocket != null) {
                if(webSocket.State != WebSocketState.Closed) {
                    // Do something???
                }
                if(webSocket.State == WebSocketState.Closed && address != null && connectionAttempts < maxConnectionAttempts) {
                    await Reconnect();
                }
            }
            else if(connectionAttempts == maxConnectionAttempts) {
                ConsoleHandlerR.Instance.AddItemToConsole(new ListItemR("Host unavailable",1));
            }
        }
    }

    private static async Task ReceiveState(ClientWebSocket webSocket)
    {
        while (webSocket.State == WebSocketState.Open)
        {
            var result = await ReceiveStringAsync();
            var message = JsonUtility.FromJson<MachineStateMessage>(result);
            if(stateObject) {
                stateObject.GetComponent<MachineState>().consumeMessage(message);
            }
            else {
                Debug.Log("No state available");
            }
        }
        if(webSocket.State == WebSocketState.Closed) {
            await Reconnect();
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
}

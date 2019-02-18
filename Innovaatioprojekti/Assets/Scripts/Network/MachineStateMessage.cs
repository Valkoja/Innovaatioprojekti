using UnityEngine;

[System.Serializable]
public class MachineStateMessage {
    public LimitWarnings limitWarnings;
    public ZeroLevel zeroLevel;
    public Angles angles;
    public Quaternions quaternions;

    public static MachineStateMessage CreateFromJSON(string jsonString)
    {
        return JsonUtility.FromJson<MachineStateMessage>(jsonString);
    }
}
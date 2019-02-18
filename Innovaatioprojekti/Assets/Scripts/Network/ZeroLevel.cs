using UnityEngine;

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
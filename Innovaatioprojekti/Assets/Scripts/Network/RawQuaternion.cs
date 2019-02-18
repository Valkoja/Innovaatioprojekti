using UnityEngine;

[System.Serializable]
public class RawQuaternion {
    public float w = 0f;
    public float x = 0f;
    public float y = 0f;
    public float z = 0f;

    public static RawQuaternion CreateFromJSON(string jsonString)
    {
        return JsonUtility.FromJson<RawQuaternion>(jsonString);
    }

    public override string ToString() {
        return $"w: {w}, x: {x}, y: {y}, z:{z}";
    }
}
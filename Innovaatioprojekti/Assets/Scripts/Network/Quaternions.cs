using UnityEngine;

[System.Serializable]
public class Quaternions {
    public RawQuaternion frame_orientation;
    public RawQuaternion main_boom_orientation;
    public RawQuaternion digging_arm_orientation;
    public RawQuaternion bucket_orientation;

    public static Angles CreateFromJSON(string jsonString)
    {
        return JsonUtility.FromJson<Angles>(jsonString);
    }
}
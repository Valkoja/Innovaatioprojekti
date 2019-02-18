using UnityEngine;

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
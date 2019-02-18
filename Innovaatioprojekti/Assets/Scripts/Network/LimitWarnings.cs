using System;
using UnityEngine;

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
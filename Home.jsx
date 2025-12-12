import { useState, useEffect } from "react";

export default function Home() {
  const [rawForm, setRawForm] = useState({
    Age: "",
    Usage_Frequency: "",
    SupportCalls: "",
    PaymentDelay: "",
    Total_spend: "",
    Last_Interaction: "",
    Churn: "",
    Gender: "",
    Contract: "",
    Subscription: "",
  });

  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [backendMessage, setBackendMessage] = useState("");

  // Check backend status
  useEffect(() => {
    fetch("http://127.0.0.1:5000/")
      .then((res) => res.text())
      .then((msg) => setBackendMessage(msg))
      .catch(() => setBackendMessage("Backend not connected"));
  }, []);

  const handleChange = (e) => {
    setRawForm({ ...rawForm, [e.target.name]: e.target.value });
  };

  const prettyLabel = (key) =>
    key
      .replace(/_/g, " ")
      .replace(/([A-Z])/g, " $1")
      .trim()
      .replace(/\b\w/g, (c) => c.toUpperCase());

  // Encode for backend
  const encodeData = () => {
    return {
      Age: Number(rawForm.Age),
      Usage_Frequency: Number(rawForm.Usage_Frequency),
      SupportCalls: Number(rawForm.SupportCalls),
      PaymentDelay: Number(rawForm.PaymentDelay),
      Total_spend: Number(rawForm.Total_spend),
      Last_Interaction: Number(rawForm.Last_Interaction),

      Churn: rawForm.Churn === "Yes" ? 1 : 0,
      Gender_Label: rawForm.Gender === "Male" ? 1 : 0,

      Contract_Length:
        rawForm.Contract === "Annual"
          ? 12
          : rawForm.Contract === "Quarterly"
          ? 3
          : 1,

      Sub_Basic: rawForm.Subscription === "Basic" ? 1 : 0,
      Sub_Premium: rawForm.Subscription === "Premium" ? 1 : 0,
      Sub_Standard: rawForm.Subscription === "Standard" ? 1 : 0,
    };
  };

  const handleTenurePredict = async () => {
    const finalData = encodeData();
    setLoading(true);
    setPrediction(null);

    try {
      const res = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(finalData),
      });

      const data = await res.json();
      setPrediction(data.tenure_prediction);
    } catch (error) {
      alert("Backend is not connected!");
    }

    setLoading(false);
  };

  return (
    <div className="flex flex-col items-center mt-10 px-4">

      {/* Backend status */}
      {/* {backendMessage && (
        <div className="mb-4 bg-green-200 text-green-800 p-3 rounded-md shadow">
          {backendMessage}
        </div>
      )} */}

      <div className="w-full max-w-lg bg-white shadow-xl p-8 rounded-2xl">
        <h2 className="text-2xl font-bold text-blue-600 text-center mb-6">
          Tenure Prediction Form
        </h2>

        {/* Numeric Inputs */}
        <div className="grid grid-cols-2 gap-4">
          {[
            "Age",
            "Usage_Frequency",
            "SupportCalls",
            "PaymentDelay",
            "Total_spend",
            "Last_Interaction",
          ].map((key) => (
            <div key={key}>
              <label className="text-gray-600 font-medium">
                {prettyLabel(key)}
              </label>
              <input
                type="number"
                name={key}
                value={rawForm[key]}
                onChange={handleChange}
                className="w-full p-2 border rounded-md mt-1 focus:outline-blue-500"
              />
            </div>
          ))}
        </div>

        {/* Dropdowns */}
        <div className="grid grid-cols-2 gap-4 mt-4">

          {/* Churn */}
          <div>
            <label className="text-gray-600 font-medium">Churn</label>
            <select
              name="Churn"
              value={rawForm.Churn}
              onChange={handleChange}
              className="w-full p-2 border rounded-md mt-1"
            >
              <option value="">Select</option>
              <option>Yes</option>
              <option>No</option>
            </select>
          </div>

          {/* Gender */}
          <div>
            <label className="text-gray-600 font-medium">Gender</label>
            <select
              name="Gender"
              value={rawForm.Gender}
              onChange={handleChange}
              className="w-full p-2 border rounded-md mt-1"
            >
              <option value="">Select</option>
              <option>Male</option>
              <option>Female</option>
            </select>
          </div>

          {/* Contract */}
          <div>
            <label className="text-gray-600 font-medium">Contract Length</label>
            <select
              name="Contract"
              value={rawForm.Contract}
              onChange={handleChange}
              className="w-full p-2 border rounded-md mt-1"
            >
              <option value="">Select</option>
              <option>Annual</option>
              <option>Monthly</option>
              <option>Quarterly</option>
            </select>
          </div>

          {/* Subscription */}
          <div>
            <label className="text-gray-600 font-medium">Subscription Type</label>
            <select
              name="Subscription"
              value={rawForm.Subscription}
              onChange={handleChange}
              className="w-full p-2 border rounded-md mt-1"
            >
              <option value="">Select</option>
              <option>Basic</option>
              <option>Standard</option>
              <option>Premium</option>
            </select>
          </div>
        </div>

        <button
          onClick={handleTenurePredict}
          className={`w-full mt-6 py-3 rounded-lg text-lg font-semibold text-white 
            ${loading ? "bg-gray-400" : "bg-blue-600 hover:bg-blue-700"}`}
          disabled={loading}
        >
          {loading ? "Predicting..." : "Predict Tenure"}
        </button>
      </div>

      {/* Prediction Card */}
      {prediction !== null && (
        <div className="mt-8 bg-green-100 shadow-lg border border-green-300 p-6 rounded-xl text-center w-full max-w-md animate-fade-in">
          <h3 className="text-2xl font-bold text-green-700">Predicted Tenure</h3>
          <p className="text-5xl font-extrabold text-green-800 mt-3">
            {prediction} Months
          </p>
        </div>
      )}

      <style>
        {`
          @keyframes fade-in {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
          }
          .animate-fade-in {
            animation: fade-in 0.6s ease-out;
          }
        `}
      </style>
    </div>
  );
}

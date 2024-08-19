// app/login/page.tsx

"use client"; // This directive makes the component a Client Component

import { useState } from "react";
import { useRouter } from "next/navigation";
import PocketBase from "pocketbase";

const pb = new PocketBase("http://127.0.0.1:8090"); // Replace with your PocketBase server URL

const LoginPage = () => {
  const [registerNo, setRegisterNo] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const router = useRouter();

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    try {
      const registerNoNumber = Number(registerNo);

      const result = await pb
        .collection("students")
        .getFirstListItem(
          `registerNo="${registerNoNumber}" && password="${password}"`
        );

      if (result) {
        console.log("Login successful:", result);

        // Store registration number in localStorage
        localStorage.setItem("registerNo", registerNo);

        // Optionally, store additional data like a token if your authentication system requires it
        // localStorage.setItem('authToken', result.token);

        setSuccess("Login successful!");
        setError(null);

        // Redirect to the home page
        router.push("/home"); // Adjust the redirect path as needed
      } else {
        setSuccess(null);
        setError("Invalid registration number or password.");
      }
    } catch (err) {
      setSuccess(null);
      setError("Login failed. Please try again.");
      console.error("Error:", err);
    }
  };

  return (
    <div className="max-w-sm mx-auto mt-10">
      <h1 className="text-2xl font-bold mb-6 text-center">Login Page</h1>
      <form
        onSubmit={handleSubmit}
        className="bg-white p-6 rounded-lg shadow-md"
      >
        <div className="mb-5">
          <label
            htmlFor="registerNo"
            className="block mb-2 text-sm font-medium text-gray-900"
          >
            Registration Number
          </label>
          <input
            type="text"
            id="registerNo"
            value={registerNo}
            onChange={(e) => setRegisterNo(e.target.value)}
            className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
            placeholder="Registration Number"
            required
          />
        </div>
        <div className="mb-5">
          <label
            htmlFor="password"
            className="block mb-2 text-sm font-medium text-gray-900"
          >
            Password
          </label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
            placeholder="Password"
            required
          />
        </div>
        <button
          type="submit"
          className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center"
        >
          Login
        </button>
      </form>
      {error && <p className="mt-4 text-red-500 text-center">{error}</p>}
      {success && <p className="mt-4 text-green-500 text-center">{success}</p>}
    </div>
  );
};

export default LoginPage;

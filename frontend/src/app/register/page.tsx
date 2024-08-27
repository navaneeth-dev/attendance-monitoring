"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import PocketBase from "pocketbase";
import Image from "next/image";

const pb = new PocketBase(process.env.NEXT_PUBLIC_POCKETBASE_URL);

const RegisterPage = () => {
  const [name, setName] = useState("");
  const [registerNo, setRegisterNo] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const router = useRouter();

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    try {
      const registerNoNumber = Number(registerNo);

      const response = await pb.collection("students").create({
        studName: name,
        registerNo: registerNoNumber,
        password, // Hash password before storing it in a real application
      });

      console.log("Response:", response);

      setSuccess("Registration successful!");
      setError(null);

      router.push("/login");
    } catch (err) {
      setSuccess(null);
      setError("Registration failed. Please try again.");
      console.error("Error:", err);
    }
  };

  return (
    <div className="max-w-sm mx-auto mt-10">
      <div className="flex justify-center items-end ">
        <Image
          src="/ov.png"
          alt="OnlyVels AMS"
          width={1280}
          height={320}
          className="h-10 w-auto"
        />
        <span className="font-medium text-xs">AMS</span>
      </div>
      <form
        onSubmit={handleSubmit}
        className="bg-white p-6 rounded-lg shadow-md"
      >
        <div className="mb-5">
          <label
            htmlFor="name"
            className="block mb-2 text-sm font-medium text-gray-900"
          >
            Your Name
          </label>
          <input
            type="text"
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
            placeholder="Name"
            required
          />
        </div>
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
          className="text-white bg-[#00aeef] hover:bg-[#008ccf] focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center"
        >
          Register
        </button>
        <div className="register mt-5">
          <p>
            Already have an account?
            <a href="/login" className="font-semibold underline">
              Login
            </a>
          </p>
        </div>
      </form>
      {error && <p className="mt-4 text-red-500 text-center">{error}</p>}
      {success && <p className="mt-4 text-green-500 text-center">{success}</p>}
    </div>
  );
};

export default RegisterPage;

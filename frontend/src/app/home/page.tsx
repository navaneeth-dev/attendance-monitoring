"use client"; // This directive makes the component a Client Component

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import PocketBase from "pocketbase";

const pb = new PocketBase("http://127.0.0.1:8090"); // Replace with your PocketBase server URL

const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return date.toISOString().split("T")[0]; // Extract date part only
};

const HomePage = () => {
  const [attendance, setAttendance] = useState<
    { date: string; percentage: number }[]
  >([]);
  const [error, setError] = useState<string | null>(null);
  const [studentName, setStudentName] = useState<string | null>(null);
  const router = useRouter();

  useEffect(() => {
    const checkLogin = async () => {
      const registerNo = localStorage.getItem("registerNo");

      if (!registerNo) {
        router.push("/login"); // Redirect to login page if not logged in
        return;
      }

      try {
        // Fetch student info
        const student = await pb
          .collection("students")
          .getFirstListItem(`registerNo="${registerNo}"`);
        setStudentName(student.studName);

        // Fetch attendance records
        const records = await pb.collection("attendance").getFullList({
          filter: `registerNo="${registerNo}"`, // Filtering by registration number
        });

        const attendanceData = records.map((record) => ({
          date: formatDate(record.date), // Format the date here
          percentage: record.percentage,
        }));

        setAttendance(attendanceData);
        setError(null);
      } catch (err) {
        setError("Failed to fetch data.");
        console.error("Error:", err);
      }
    };

    checkLogin();
  }, [router]);

  const handleLogout = () => {
    localStorage.removeItem("registerNo");
    router.push("/login");
  };

  return (
    <>
      <div className="w-full border-b">
        <header className="max-w-screen-xl bg-white mx-auto">
          <nav className="flex justify-between items-center p-4">
            <div className="flex items-center space-x-4">
              <h1 className="text-2xl font-bold">
                Attendance Monitoring System
              </h1>
              
            </div>
            <div>
            {studentName && (
                <span className="text-sm text-gray-700 mr-5">
                  Welcome, {studentName}
                </span>
              )}
              <button
                onClick={handleLogout}
                className="text-white bg-red-600 hover:bg-red-700 focus:ring-4 focus:outline-none focus:ring-red-300 font-medium rounded-lg text-sm px-4 py-2"
              >
                Logout
              </button>
            </div>
          </nav>
        </header>
      </div>
      <div className="max-w-screen-xl bg-white mx-auto">
        {error && <p className="text-red-500 text-center mt-4">{error}</p>}
        <table className="max-w-screen-xl min-w-full bg-white border border-gray-200 rounded-lg shadow-md mt-6">
          <thead>
            <tr className="bg-gray-100 border-b">
              <th className="py-2 px-4 text-left text-sm font-medium text-gray-900">
                Date
              </th>
              <th className="py-2 px-4 text-left text-sm font-medium text-gray-900">
                Percentage
              </th>
            </tr>
          </thead>
          <tbody>
            {attendance.length > 0 ? (
              attendance.map((record, index) => (
                <tr key={index} className="border-b">
                  <td className="py-2 px-4 text-sm text-gray-900">
                    {record.date}
                  </td>
                  <td className="py-2 px-4 text-sm text-gray-900">
                    {record.percentage}%
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={2} className="py-2 px-4 text-center text-gray-500">
                  No records found
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </>
  );
};

export default HomePage;

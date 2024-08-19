"use client"; // This directive makes the component a Client Component

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import PocketBase from "pocketbase";
import ApexCharts from "react-apexcharts"; // Import ApexCharts

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
  const [chartOptions, setChartOptions] = useState({
    chart: {
      id: "attendance-chart",
      toolbar: {
        show: false,
      },
    },
    xaxis: {
      categories: [],
      title: {
        text: "Month",
      },
      labels: {
        style: {
          colors: "#6B7280",
        },
      },
    },
    yaxis: {
      min: 0,
      max: 100,
      tickAmount: 10,
      labels: {
        formatter: (val: number) => `${val}%`,
        style: {
          colors: "#6B7280",
        },
      },
      title: {
        text: "Percentage",
      },
    },
    title: {
      text: "Monthly Attendance Percentage",
      style: {
        fontSize: "16px",
        fontWeight: "bold",
      },
    },
    grid: {
      borderColor: "#e5e7eb",
    },
    colors: ["#4f46e5"], // Line color
    stroke: {
      curve: "smooth",
      width: 2, // Line thickness
    },
    markers: {
      size: 6, // Size of the markers
      colors: ["#4f46e5"], // Color of the markers
      strokeColors: "#fff", // Stroke color of the markers
      strokeWidth: 2, // Stroke width of the markers
      hover: {
        size: 8, // Size of the markers on hover
        sizeOffset: 3, // Offset for the hover effect
      },
    },
    tooltip: {
      shared: true,
      intersect: false,
    },
  });
  const [chartSeries, setChartSeries] = useState([
    {
      name: "Attendance",
      data: [],
    },
  ]);
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
          date: formatDate(record.date),
          percentage: record.percentage,
        }));

        setAttendance(attendanceData);
        setError(null);

        // Prepare data for the chart
        const months = attendanceData.map((record) => record.date);
        const percentages = attendanceData.map((record) => record.percentage);

        setChartOptions((prevOptions) => ({
          ...prevOptions,
          xaxis: { categories: months },
        }));
        setChartSeries([
          {
            name: "Attendance",
            data: percentages,
          },
        ]);
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
      <div className="w-full ">
        <header className="max-w-screen-xl mx-auto bg-white shadow-md rounded-md">
          <nav className="flex justify-between items-center p-4">
            <div className="flex items-center space-x-4">
              <h1 className="text-2xl font-extrabold text-gray-800">
                Attendance Monitoring System
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              {studentName && (
                <span className="text-sm text-gray-600">
                  Welcome, {studentName}
                </span>
              )}
              <button
                onClick={handleLogout}
                className="bg-red-600 text-white hover:bg-red-700 focus:ring-4 focus:outline-none focus:ring-red-300 font-medium rounded-lg text-sm px-4 py-2"
              >
                Logout
              </button>
            </div>
          </nav>
        </header>
      </div>
      <div className="max-w-screen-xl mx-auto mt-4">
        {error && <p className="text-red-500 text-center mt-4">{error}</p>}
        <div className="bg-white border border-gray-200 rounded-lg shadow-md p-4 mb-6">
          <ApexCharts
            type="line"
            options={chartOptions}
            series={chartSeries}
            height={350}
          />
        </div>
        <div className="bg-white border border-gray-200 rounded-lg shadow-md p-4">
          <table className="min-w-full bg-white border border-gray-200 rounded-lg shadow-md">
            <thead>
              <tr className="bg-gray-100 border-b">
                <th className="py-3 px-4 text-left text-sm font-medium text-gray-900">
                  Date
                </th>
                <th className="py-3 px-4 text-left text-sm font-medium text-gray-900">
                  Percentage
                </th>
              </tr>
            </thead>
            <tbody>
              {attendance.length > 0 ? (
                attendance.map((record, index) => (
                  <tr key={index} className="border-b">
                    <td className="py-3 px-4 text-sm text-gray-900">
                      {record.date}
                    </td>
                    <td className="py-3 px-4 text-sm text-gray-900">
                      {record.percentage}%
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td
                    colSpan={2}
                    className="py-3 px-4 text-center text-gray-500"
                  >
                    No records found
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
};

export default HomePage;
